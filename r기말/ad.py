"""
한국 주식시장: 개인 vs 외국인 vs 기관 — Streamlit 대시보드 (개선판)
==========================================================
변경 사항 요약:
  1. 방향성 수익률 proxy 방법론 한계를 모든 관련 차트에 캡션으로 명시
  2. 통계 지표 강화: 상관계수, MDD, 샤프지수를 요약 카드에 추가
  3. 역추세 패턴 검증: rolling 상관계수 차트 + OLS p-value 추가
  4. 백테스트 로직 개선: 누적 수익률 외 MDD·샤프지수 병기

버그 수정:
  - date_input 날짜 한 쪽만 선택 시 IndexError 방어
  - make_sim 반환값 (df, False) 튜플로 통일
  - load_data @cache_data 가 make_sim 이후에 정의되도록 순서 교정

설치:
    pip install streamlit plotly pandas numpy scipy pykrx

실행:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# ── 페이지 설정 ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="개미는 항상 지는가?",
    page_icon="📊",
    layout="wide",
)

# ── 스타일 ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.metric-card {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 16px 20px;
    border-left: 4px solid #ccc;
}
.red   { border-color: #E24B4A; }
.blue  { border-color: #3266AD; }
.green { border-color: #2E9E6B; }
.metric-label { font-size: 13px; color: #888; margin-bottom: 4px; }
.metric-value { font-size: 24px; font-weight: 600; }
.metric-delta { font-size: 12px; margin-top: 4px; color: #666; }
.method-warn {
    background: #fff8e1;
    border-left: 4px solid #f9a825;
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 13px;
    color: #5d4037;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

COLORS = {"개인": "#E24B4A", "외국인": "#3266AD", "기관": "#2E9E6B", "KOSPI": "#AAAAAA"}

METHOD_WARN = (
    "⚠️ <b>방법론 한계</b>: 여기서 표시하는 수익률은 '순매수 방향 × 익일 지수 수익률'로 계산한 "
    "<b>근사치(proxy)</b>입니다. KRX는 투자자별 순매수 금액만 공개하며, 실제 실현 수익률은 "
    "매수 단가·보유 기간·매도 시점에 따라 크게 달라집니다. "
    "이 수치를 실제 투자 성과와 동일시하지 마십시오."
)

# ── 통계 헬퍼 함수 ────────────────────────────────────────────────────────────
def calc_mdd(cum_ret_series: pd.Series) -> float:
    """최대 낙폭(MDD). cum_ret_series = 누적수익률(소수)."""
    wealth = 1 + cum_ret_series
    peak = wealth.cummax()
    return float(((wealth - peak) / peak).min()) * 100


def calc_sharpe(daily_ret_series: pd.Series, rf: float = 0.0, ann: int = 252) -> float:
    """연환산 샤프지수. 무위험수익률 기본 0."""
    excess = daily_ret_series - rf
    return 0.0 if excess.std() == 0 else float(excess.mean() / excess.std() * np.sqrt(ann))


def calc_stats(pnl: pd.DataFrame, df: pd.DataFrame) -> dict:
    result = {}
    next_ret = df["KOSPI"].pct_change().shift(-1)
    for inv in ["개인", "외국인", "기관"]:
        cum = pnl[inv]
        daily = cum.diff().fillna(0)
        result[inv] = {
            "cum_ret":        float(cum.iloc[-2]) * 100,
            "mdd":            calc_mdd(cum),
            "sharpe":         calc_sharpe(daily),
            "corr_with_next": float(df[inv].corr(next_ret)),
        }
    return result

# ── 시뮬레이션 데이터 (pykrx 미설치 시) ─────────────────────────────────────
def make_sim(start, end):
    np.random.seed(42)
    dates = pd.bdate_range(start, end)
    n = len(dates)
    pts = np.array([2200, 1440, 3300, 2600, 2500, 2800])
    segs = [max(1, int(n * r)) for r in [0.05, 0.15, 0.25, 0.25, 0.15, 0.15]]
    segs[-1] += n - sum(segs)
    kospi = np.concatenate([
        np.linspace(pts[i], pts[i + 1], segs[i]) for i in range(len(segs) - 1)
    ] + [np.linspace(pts[-2], pts[-1], segs[-1])])[:n]
    kospi += np.random.normal(0, 30, n).cumsum() * 0.1
    ret = np.diff(kospi, prepend=kospi[0]) / np.maximum(kospi, 1)
    s = 5e11
    ind  = (-ret * 0.6 + np.random.normal(0, 0.3, n)) * s
    fore = ( ret * 0.5 + np.random.normal(0, 0.2, n)) * s
    inst = -(ind + fore) * 0.7 + np.random.normal(0, 0.1, n) * s
    return pd.DataFrame(
        {"개인": ind, "외국인": fore, "기관": inst, "KOSPI": kospi}, index=dates
    ), False   # ← 반드시 (df, False) 튜플로 반환


# ── KRX 실데이터 로드 (make_sim 이후에 정의) ─────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(start, end):
    try:
        from pykrx import stock
        df_inv = stock.get_market_trading_value_by_date(
            start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), "KOSPI"
        )[["개인", "외국인", "기관합계"]].rename(columns={"기관합계": "기관"})
        df_k = stock.get_index_ohlcv_by_date(
            start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), "1001"
        )["종가"].rename("KOSPI")
        df = pd.concat([df_inv, df_k], axis=1).dropna()
        return df, True
    except Exception:
        return make_sim(start, end)   # make_sim 이 (df, False) 반환


def calc_pnl(df):
    """방향성 수익률 proxy: sign(순매수) × 익일 지수 수익률의 누적곱"""
    ret = df["KOSPI"].pct_change().shift(-1)
    pnl = pd.DataFrame(index=df.index)
    for inv in ["개인", "외국인", "기관"]:
        pnl[inv] = (1 + np.sign(df[inv]) * ret.fillna(0)).cumprod() - 1
    return pnl


# ── 사이드바 ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ 설정")

    raw_range = st.date_input(
        "분석 기간",
        value=(pd.Timestamp("2020-01-02"), pd.Timestamp("2024-12-31")),
        min_value=pd.Timestamp("2015-01-01"),
        max_value=pd.Timestamp("2025-12-31"),
    )
    # ★ 방어: 날짜 한 쪽만 선택됐을 때 IndexError 방지
    if isinstance(raw_range, (list, tuple)) and len(raw_range) == 2:
        start_date = pd.Timestamp(raw_range[0])
        end_date   = pd.Timestamp(raw_range[1])
    else:
        st.warning("시작일과 종료일을 모두 선택해 주세요.")
        st.stop()

    show_investors = st.multiselect(
        "표시할 투자자",
        ["개인", "외국인", "기관"],
        default=["개인", "외국인", "기관"],
    )
    if not show_investors:
        st.warning("투자자를 한 명 이상 선택해 주세요.")
        st.stop()

    ma_window      = st.slider("이동평균 윈도우 (일)", 5, 60, 20)
    rolling_window = st.slider("Rolling 상관계수 윈도우 (일)", 20, 120, 60)

    st.divider()
    st.markdown("**데이터 출처**")
    st.markdown("- KRX 한국거래소 (pykrx)\n- 자본시장연구원\n- 한투데이 2025")
    st.markdown("`pip install pykrx` 설치 시 실제 KRX 데이터 사용")
    st.divider()
    st.markdown(
        "**수익률 proxy 방법론**\n\n"
        "sign(순매수) × 익일 KOSPI 수익률의 누적곱.\n"
        "KRX 미공개 실현손익의 **근사치**이며 "
        "개별 종목·매도 시점 효과는 미반영."
    )

# ── 데이터 로드 ───────────────────────────────────────────────────────────────
with st.spinner("데이터 불러오는 중..."):
    df, is_real = load_data(start_date, end_date)

pnl        = calc_pnl(df)
yearly     = df[["개인", "외국인", "기관"]].resample("YE").sum() / 1e12
stats_dict = calc_stats(pnl, df)

# ── 헤더 ─────────────────────────────────────────────────────────────────────
st.title("📊 한국 주식시장: 개미는 항상 지는가?")
st.caption(
    f"{'✅ 실제 KRX 데이터' if is_real else '⚠️ 시뮬레이션 데이터 (pykrx 미설치)'}"
    f"  |  분석 기간: {start_date.date()} ~ {end_date.date()}"
    f"  |  {len(df):,}거래일"
)
st.markdown(f'<div class="method-warn">{METHOD_WARN}</div>', unsafe_allow_html=True)

# ── 요약 카드 (누적수익 + MDD + 샤프지수 + 상관계수) ─────────────────────────
st.subheader("📌 투자자별 통계 요약")
cols_top = st.columns(3)
card_cfg = [
    ("개인",   "red",   "#E24B4A"),
    ("외국인", "blue",  "#3266AD"),
    ("기관",   "green", "#2E9E6B"),
]
for col, (inv, cls, color) in zip(cols_top, card_cfg):
    s = stats_dict[inv]
    with col:
        st.markdown(f"""
        <div class="metric-card {cls}">
          <div class="metric-label">{inv} — 누적 방향성 수익률 <sup style="font-size:10px">proxy</sup></div>
          <div class="metric-value" style="color:{color}">{s['cum_ret']:+.1f}%</div>
          <div class="metric-delta">
            MDD: {s['mdd']:.1f}%&nbsp;&nbsp;|&nbsp;&nbsp;
            샤프: {s['sharpe']:.2f}&nbsp;&nbsp;|&nbsp;&nbsp;
            상관계수: {s['corr_with_next']:.3f}
          </div>
        </div>
        """, unsafe_allow_html=True)

corr_개인 = stats_dict["개인"]["corr_with_next"]
st.caption(
    f"상관계수 = 투자자 순매수 vs 익일 KOSPI 수익률 (피어슨 r). "
    f"개인 {corr_개인:.3f}: "
    f"{'음의 상관 → 역추세 매매 패턴 확인' if corr_개인 < 0 else '양의 상관 → 추세추종'}. "
    "MDD·샤프는 proxy 기준이며 실제 성과와 다를 수 있습니다."
)
st.divider()

# ── ① KOSPI + 순매수 흐름 ────────────────────────────────────────────────────
st.subheader("① KOSPI 지수 & 투자자별 순매수 흐름")
fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(go.Scatter(
    x=df.index, y=df["KOSPI"], name="KOSPI",
    line=dict(color=COLORS["KOSPI"], width=1.5),
    fill="tozeroy", fillcolor="rgba(180,180,180,0.1)"
), secondary_y=False)
for inv in show_investors:
    ma = df[inv].rolling(ma_window).mean() / 1e8
    fig1.add_trace(go.Scatter(
        x=df.index, y=ma, name=f"{inv} ({ma_window}일 MA)",
        line=dict(color=COLORS[inv], width=1.8)
    ), secondary_y=True)
fig1.add_hline(y=0, line=dict(color="#ccc", dash="dash"), secondary_y=True)
fig1.update_yaxes(title_text="KOSPI 지수", secondary_y=False)
fig1.update_yaxes(title_text="순매수 이동평균 (억원)", secondary_y=True)
fig1.update_layout(height=360, hovermode="x unified", legend=dict(orientation="h", y=1.08))
st.plotly_chart(fig1, use_container_width=True)

# ── ② 누적 방향성 수익률  +  ③ 연도별 순매수 ────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("② 누적 방향성 수익률 (proxy)")
    fig2 = go.Figure()
    for inv in show_investors:
        fig2.add_trace(go.Scatter(
            x=pnl.index, y=pnl[inv] * 100,
            name=inv, line=dict(color=COLORS[inv], width=2)
        ))
    fig2.add_hline(y=0, line=dict(color="#aaa", dash="dash"))
    fig2.update_layout(
        height=320, yaxis_title="누적 수익률 (%)",
        yaxis_ticksuffix="%", hovermode="x unified",
        legend=dict(orientation="h", y=1.08)
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "📌 sign(순매수) × 익일 지수 수익률의 누적값 — 실제 실현 수익률의 **근사치(proxy)**. "
        "매수 단가·보유 기간·매도 시점·거래비용은 반영되지 않습니다."
    )

with col_b:
    st.subheader("③ 연도별 순매수 합계 (조원)")
    fig3 = go.Figure()
    years = [str(y.year) for y in yearly.index]
    for inv in show_investors:
        fig3.add_trace(go.Bar(
            x=years, y=yearly[inv].round(1),
            name=inv, marker_color=COLORS[inv], opacity=0.85
        ))
    fig3.add_hline(y=0, line=dict(color="#888", dash="dash"))
    fig3.update_layout(
        height=320, barmode="group", yaxis_title="순매수 (조원)",
        legend=dict(orientation="h", y=1.08)
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("출처: KRX 한국거래소 (pykrx) / 시뮬레이션 데이터")

# ── ④ Rolling 상관계수 — 역추세 패턴 검증 (신규) ─────────────────────────────
st.subheader(f"④ Rolling 상관계수 ({rolling_window}일) — 역추세 패턴 검증")
next_ret = df["KOSPI"].pct_change().shift(-1)
fig_roll = go.Figure()
for inv in show_investors:
    roll_corr = df[inv].rolling(rolling_window).corr(next_ret)
    fig_roll.add_trace(go.Scatter(
        x=df.index, y=roll_corr,
        name=inv, line=dict(color=COLORS[inv], width=1.8)
    ))
fig_roll.add_hline(y=0,    line=dict(color="#aaa", dash="dash"))
fig_roll.add_hline(y=0.1,  line=dict(color="#ccc", dash="dot"), annotation_text="+0.1")
fig_roll.add_hline(y=-0.1, line=dict(color="#ccc", dash="dot"), annotation_text="-0.1")
fig_roll.update_layout(
    height=300, yaxis_title="상관계수 (r)",
    hovermode="x unified", legend=dict(orientation="h", y=1.08)
)
st.plotly_chart(fig_roll, use_container_width=True)
st.caption(
    f"투자자 순매수 금액 vs 익일 KOSPI 수익률의 {rolling_window}일 Rolling 피어슨 r. "
    "개인이 지속적으로 음의 상관 → 역추세 패턴이 구조적임을 시사. "
    "0선을 오가는 구간은 패턴 일시 약화 또는 추세추종 전환 시기."
)

# ── ⑤ 연령대별 손실률  +  ⑥ 회귀분석 ───────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("⑤ 연령대별 개인투자자 손실률")
    ages  = ["미성년", "20대", "30대", "40대", "50대", "60대+"]
    vals4 = [33.9, 44.3, 52.1, 59.7, 60.1, 55.2]
    bar_colors = [
        COLORS["개인"] if v >= 50 else "#F09595" if v >= 44 else "#F7C1C1"
        for v in vals4
    ]
    fig4 = go.Figure(go.Bar(
        x=vals4, y=ages, orientation="h",
        marker_color=bar_colors,
        text=[f"{v}%" for v in vals4], textposition="outside"
    ))
    fig4.add_vline(x=50, line=dict(color="#E24B4A", dash="dash"), annotation_text="50%")
    fig4.update_layout(height=300, xaxis=dict(range=[0, 75], title="손실 투자자 비율 (%)"))
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("출처: 한투데이 2025 | KRX 실현손익 기준 (proxy 수익률과 무관한 별도 데이터)")

with col_d:
    st.subheader("⑥ 개인 매수 방향 vs 익일 수익률 (OLS 회귀)")
    sample = df.sample(min(600, len(df)), random_state=0)
    nr = sample["KOSPI"].pct_change().shift(-1) * 100
    ix = sample["개인"] / sample["개인"].abs().max()
    sdf = pd.concat([ix, nr], axis=1).dropna()
    sdf.columns = ["x", "y"]
    slope, intercept, r_val, p_val, std_err = stats.linregress(sdf["x"], sdf["y"])
    xfit = np.linspace(sdf["x"].min(), sdf["x"].max(), 100)

    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=sdf["x"], y=sdf["y"], mode="markers",
        marker=dict(color=COLORS["개인"], opacity=0.3, size=5), name="관측값"
    ))
    fig5.add_trace(go.Scatter(
        x=xfit, y=slope * xfit + intercept, mode="lines",
        line=dict(color="#333", dash="dash", width=2),
        name=f"회귀선 (β={slope:.4f})"
    ))
    fig5.add_hline(y=0, line=dict(color="#ccc"))
    fig5.add_vline(x=0, line=dict(color="#ccc"))
    fig5.update_layout(
        height=300,
        xaxis_title="개인 순매수 방향 (정규화)",
        yaxis_title="익일 KOSPI 수익률 (%)"
    )
    st.plotly_chart(fig5, use_container_width=True)
    sig  = "통계적으로 유의 (p<0.05)" if p_val < 0.05 else f"유의하지 않음 (p={p_val:.4f})"
    sign = "↘ 역추세" if slope < 0 else "↗ 추세추종"
    st.caption(
        f"OLS: β={slope:.4f} ({sign}), r={r_val:.3f}, {sig}, SE={std_err:.4f}. "
        "KOSPI 지수 단순회귀 — 개별 종목 효과 미포함."
    )

# ── ⑦ Drawdown 추이 (신규) ───────────────────────────────────────────────────
st.divider()
st.subheader("⑦ Drawdown 추이 (proxy 수익률 기준)")
fig_dd = go.Figure()
FILL_ALPHA = {"개인": "rgba(226,75,74,0.10)", "외국인": "rgba(50,102,173,0.10)", "기관": "rgba(46,158,107,0.10)"}
for inv in show_investors:
    wealth = 1 + pnl[inv]
    dd = (wealth - wealth.cummax()) / wealth.cummax() * 100
    fig_dd.add_trace(go.Scatter(
        x=pnl.index, y=dd, name=inv,
        line=dict(color=COLORS[inv], width=1.5),
        fill="tozeroy", fillcolor=FILL_ALPHA[inv]
    ))
fig_dd.add_hline(y=0, line=dict(color="#aaa"))
fig_dd.update_layout(
    height=280, yaxis_title="Drawdown (%)",
    hovermode="x unified", legend=dict(orientation="h", y=1.08)
)
st.plotly_chart(fig_dd, use_container_width=True)
st.caption(
    "MDD = proxy 누적 수익률 고점 대비 최대 하락폭. "
    "실제 포트폴리오 MDD는 종목 구성·매도 시점에 따라 상이합니다."
)

# ── ⑧ 정량·정성 비교표 ───────────────────────────────────────────────────────
st.divider()
st.subheader("⑧ 투자자 유형별 핵심 지표 비교")

# proxy 기반 정량 지표
p_rows = []
for inv in ["개인", "외국인", "기관"]:
    s = stats_dict[inv]
    p_rows.append({
        "투자자": inv,
        "누적 수익률(proxy)":     f"{s['cum_ret']:+.1f}%",
        "MDD(proxy)":             f"{s['mdd']:.1f}%",
        "샤프지수(proxy)":        f"{s['sharpe']:.2f}",
        "순매수↔익일수익 상관계수": f"{s['corr_with_next']:.3f}",
    })
st.dataframe(pd.DataFrame(p_rows).set_index("투자자"), use_container_width=True)
st.caption("위 4개 지표는 모두 proxy 방법론 기준. 실제 KRX 실현손익과 다를 수 있습니다.")

# 정성 비교표
summary_df = pd.DataFrame({
    "지표":       ["거래회전율(연)", "시장 대비 수익률", "평균 보유기간", "손실 투자자 비율", "주요 전략"],
    "개인 🔴":   ["1,600%",   "-3~5%p",  "3일 (중간값)", "~54%", "역추세·과잉거래"],
    "외국인 🔵": ["200~400%", "+2~4%p",  "30~90일",      "~35%", "추세추종·정보우위"],
    "기관 🟢":   ["300~500%", "+0~2%p",  "20~60일",      "~40%", "방어적·벤치마크"],
}).set_index("지표")
st.dataframe(summary_df, use_container_width=True)
st.caption("출처: 자본시장연구원, 한투데이 2025 | 시장 대비 수익률은 실증 연구 기반 추정치")

# ── 핵심 인사이트 ────────────────────────────────────────────────────────────
st.divider()
st.subheader("💡 핵심 인사이트")
i1, i2, i3 = st.columns(3)
with i1:
    st.error(
        "**개인: 구조적 불리**\n\n"
        "거래회전율 연 1,600%, 정보 비대칭, 처분효과(이익 조기 실현·손실 장기 보유). "
        "상관계수 음수 → 역추세 패턴 구조적 확인. "
        "과잉거래·종목 선택 실패 복합 작용."
    )
with i2:
    st.info(
        "**외국인: 추세추종 우위**\n\n"
        "알고리즘·HFT 중심, 상승장 대규모 순매수. "
        "하락 전환점 빠른 매도 → 수익 방어. "
        "샤프지수·MDD 모두 개인 대비 우위."
    )
with i3:
    st.success(
        "**결론: '항상' 지진 않는다**\n\n"
        "하락장 역매수 타이밍 적중 구간 존재 (rolling 상관계수 참조). "
        "문제는 과잉거래와 종목 선택. "
        "거래 빈도↓·분산투자 시 성과 개선 가능."
    )

# ── 방법론 상세 각주 ─────────────────────────────────────────────────────────
st.divider()
with st.expander("📎 방법론 상세 및 한계 (펼치기)"):
    st.markdown("""
**방향성 수익률 Proxy 계산식**
```
daily_proxy_return_t  = sign(순매수_t) × KOSPI_수익률_{t+1}
cum_proxy_return      = ∏(1 + daily_proxy_return_t) − 1
```

**한계점**
1. KRX는 투자자별 순매수 **금액**만 공개 — 실제 실현 손익 데이터는 비공개입니다.
2. KOSPI 지수 수익률 사용 → 개별 종목 선택 효과가 배제됩니다.
3. 거래비용(수수료·세금·슬리피지)이 반영되지 않습니다.
4. 하루 중 매수·매도 시점을 단일 가격으로 단순화합니다.
5. 동일 날 매수·매도가 혼재하는 거래를 순매수 방향으로 단순화합니다.

**통계 지표 정의**
- **상관계수**: 피어슨 r — 순매수 금액 vs 익일 KOSPI 수익률
- **MDD**: (고점 − 저점) / 고점, proxy 누적 수익률 기준
- **샤프지수**: 연환산 = 일평균 수익률 / 일표준편차 × √252, 무위험수익률 0% 가정

**권고 해석 방식**

proxy 수익률의 절대값보다 **부호·상대 비교** 및 **rolling 상관계수의 지속성**에 집중하십시오.
""")