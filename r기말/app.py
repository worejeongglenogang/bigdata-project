"""
한국 주식시장: 개인 vs 외국인 vs 기관 — Streamlit 대시보드
==========================================================
설치:
    pip install streamlit plotly pandas numpy pykrx

실행:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── 페이지 설정 ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="개미는 항상 지는가?",
    page_icon="📊",
    layout="wide",
)

# ── 스타일 ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.metric-card {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 16px 20px;
    border-left: 4px solid #ccc;
}
.red { border-color: #E24B4A; }
.blue { border-color: #3266AD; }
.green { border-color: #2E9E6B; }
.metric-label { font-size: 13px; color: #888; margin-bottom: 4px; }
.metric-value { font-size: 26px; font-weight: 600; }
.metric-delta { font-size: 12px; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

COLORS = {"개인": "#E24B4A", "외국인": "#3266AD", "기관": "#2E9E6B", "KOSPI": "#AAAAAA"}

# ── 데이터 수집 / 시뮬레이션 ───────────────────────────────────────────────────
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
        return make_sim(start, end), False


def make_sim(start, end):
    np.random.seed(42)
    dates = pd.bdate_range(start, end)
    n = len(dates)
    pts = np.array([2200, 1440, 3300, 2600, 2500, 2800])
    segs = [max(1, int(n * r)) for r in [0.05, 0.15, 0.25, 0.25, 0.15, 0.15]]
    segs[-1] += n - sum(segs)
    kospi = np.concatenate([
        np.linspace(pts[i], pts[i+1], segs[i]) for i in range(len(segs)-1)
    ] + [np.linspace(pts[-2], pts[-1], segs[-1])])[:n]
    kospi += np.random.normal(0, 30, n).cumsum() * 0.1
    ret = np.diff(kospi, prepend=kospi[0]) / np.maximum(kospi, 1)
    s = 5e11
    ind =  (-ret * 0.6 + np.random.normal(0, 0.3, n)) * s
    fore = ( ret * 0.5 + np.random.normal(0, 0.2, n)) * s
    inst = -(ind + fore) * 0.7 + np.random.normal(0, 0.1, n) * s
    return pd.DataFrame({"개인": ind, "외국인": fore, "기관": inst, "KOSPI": kospi}, index=dates)


def calc_pnl(df):
    ret = df["KOSPI"].pct_change().shift(-1)
    pnl = pd.DataFrame(index=df.index)
    for inv in ["개인", "외국인", "기관"]:
        pnl[inv] = (1 + np.sign(df[inv]) * ret.fillna(0)).cumprod() - 1
    return pnl


# ── 사이드바 ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ 설정")
    date_range = st.date_input(
        "분석 기간",
        value=(pd.Timestamp("2020-01-02"), pd.Timestamp("2024-12-31")),
        min_value=pd.Timestamp("2015-01-01"),
        max_value=pd.Timestamp("2025-12-31"),
    )
    show_investors = st.multiselect(
        "표시할 투자자",
        ["개인", "외국인", "기관"],
        default=["개인", "외국인", "기관"],
    )
    ma_window = st.slider("이동평균 윈도우 (일)", 5, 60, 20)
    st.divider()
    st.markdown("**데이터 출처**")
    st.markdown("- KRX 한국거래소 (pykrx)\n- 자본시장연구원\n- 한투데이 2025")
    st.markdown("`pip install pykrx` 설치 시\n실제 KRX 데이터 사용")

start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])

# ── 데이터 로드 ────────────────────────────────────────────────────────────────
with st.spinner("데이터 불러오는 중..."):
    df, is_real = load_data(start_date, end_date)
pnl = calc_pnl(df)
yearly = df[["개인", "외국인", "기관"]].resample("YE").sum() / 1e12

# ── 헤더 ──────────────────────────────────────────────────────────────────────
st.title("📊 한국 주식시장: 개미는 항상 지는가?")
st.caption(
    f"{'✅ 실제 KRX 데이터' if is_real else '⚠️ 시뮬레이션 데이터 (pykrx 미설치)'}"
    f"  |  분석 기간: {start_date.date()} ~ {end_date.date()}"
    f"  |  {len(df):,}거래일"
)

# ── 요약 지표 카드 ─────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
final_ret = {inv: pnl[inv].iloc[-2] * 100 for inv in ["개인", "외국인", "기관"]}
corr = df["개인"].corr(df["KOSPI"].pct_change().shift(-1))

with c1:
    v = final_ret["개인"]
    st.markdown(f"""<div class="metric-card red">
    <div class="metric-label">개인 누적 성과</div>
    <div class="metric-value" style="color:#E24B4A">{v:+.1f}%</div>
    <div class="metric-delta">{'▲' if v>0 else '▼'} 방향성 기준</div>
    </div>""", unsafe_allow_html=True)

with c2:
    v = final_ret["외국인"]
    st.markdown(f"""<div class="metric-card blue">
    <div class="metric-label">외국인 누적 성과</div>
    <div class="metric-value" style="color:#3266AD">{v:+.1f}%</div>
    <div class="metric-delta">{'▲' if v>0 else '▼'} 방향성 기준</div>
    </div>""", unsafe_allow_html=True)

with c3:
    v = final_ret["기관"]
    st.markdown(f"""<div class="metric-card green">
    <div class="metric-label">기관 누적 성과</div>
    <div class="metric-value" style="color:#2E9E6B">{v:+.1f}%</div>
    <div class="metric-delta">{'▲' if v>0 else '▼'} 방향성 기준</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""<div class="metric-card">
    <div class="metric-label">개인 역추세 상관계수</div>
    <div class="metric-value">{corr:.3f}</div>
    <div class="metric-delta">{'음의 상관 → 역추세 매매' if corr < 0 else '양의 상관 → 추세 추종'}</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── 차트 1: KOSPI + 투자자 순매수 ─────────────────────────────────────────────
st.subheader("① KOSPI 지수 & 투자자별 순매수 흐름")
fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(go.Scatter(
    x=df.index, y=df["KOSPI"],
    name="KOSPI", line=dict(color=COLORS["KOSPI"], width=1.5),
    fill="tozeroy", fillcolor="rgba(180,180,180,0.1)"
), secondary_y=False)
for inv in show_investors:
    ma = df[inv].rolling(ma_window).mean() / 1e8
    fig1.add_trace(go.Scatter(
        x=df.index, y=ma,
        name=f"{inv} ({ma_window}일MA)",
        line=dict(color=COLORS[inv], width=1.8)
    ), secondary_y=True)
fig1.add_hline(y=0, line=dict(color="#ccc", dash="dash"), secondary_y=True)
fig1.update_yaxes(title_text="KOSPI 지수", secondary_y=False)
fig1.update_yaxes(title_text="순매수 (억원)", secondary_y=True)
fig1.update_layout(height=360, hovermode="x unified", legend=dict(orientation="h", y=1.08))
st.plotly_chart(fig1, use_container_width=True)

# ── 차트 2+3 ──────────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("② 누적 방향성 성과")
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

# ── 차트 4+5 ──────────────────────────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("④ 연령대별 개인투자자 손실률")
    ages  = ["미성년", "20대", "30대", "40대", "50대", "60대+"]
    vals4 = [33.9, 44.3, 52.1, 59.7, 60.1, 55.2]
    bar_colors = [COLORS["개인"] if v >= 50 else "#F09595" if v >= 44 else "#F7C1C1" for v in vals4]
    fig4 = go.Figure(go.Bar(
        x=vals4, y=ages, orientation="h",
        marker_color=bar_colors,
        text=[f"{v}%" for v in vals4], textposition="outside"
    ))
    fig4.add_vline(x=50, line=dict(color="#E24B4A", dash="dash"), annotation_text="50%")
    fig4.update_layout(height=300, xaxis=dict(range=[0, 75], title="손실 투자자 비율 (%)"))
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("출처: 한투데이 2025")

with col_d:
    st.subheader("⑤ 개인 매수 방향 vs 익일 수익률")
    sample = df.sample(min(600, len(df)), random_state=0)
    nr = sample["KOSPI"].pct_change().shift(-1) * 100
    ix = sample["개인"] / sample["개인"].abs().max()
    sdf = pd.concat([ix, nr], axis=1).dropna()
    sdf.columns = ["x", "y"]
    z = np.polyfit(sdf["x"], sdf["y"], 1)
    xfit = np.linspace(sdf["x"].min(), sdf["x"].max(), 100)
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=sdf["x"], y=sdf["y"], mode="markers",
        marker=dict(color=COLORS["개인"], opacity=0.3, size=5), name="관측값"
    ))
    fig5.add_trace(go.Scatter(
        x=xfit, y=np.polyval(z, xfit),
        mode="lines", line=dict(color="#333", dash="dash", width=2), name="추세선"
    ))
    fig5.add_hline(y=0, line=dict(color="#ccc")); fig5.add_vline(x=0, line=dict(color="#ccc"))
    fig5.update_layout(
        height=300,
        xaxis_title="개인 순매수 방향 (정규화)",
        yaxis_title="익일 KOSPI 수익률 (%)"
    )
    st.plotly_chart(fig5, use_container_width=True)
    slope_sign = "↘ 역추세 (살수록 다음날 하락)" if z[0] < 0 else "↗ 추세추종"
    st.caption(f"추세선 기울기: {z[0]:.4f}  {slope_sign}")

# ── 요약 테이블 ────────────────────────────────────────────────────────────────
st.divider()
st.subheader("⑥ 투자자 유형별 핵심 지표 비교")
summary_df = pd.DataFrame({
    "지표": ["거래회전율(연)", "시장 대비 수익률", "평균 보유기간", "손실 투자자 비율", "주요 전략"],
    "개인 🔴": ["1,600%", "-3~5%p", "3일 (중간값)", "~54%", "역추세·과잉거래"],
    "외국인 🔵": ["200~400%", "+2~4%p", "30~90일", "~35%", "추세추종·정보우위"],
    "기관 🟢": ["300~500%", "+0~2%p", "20~60일", "~40%", "방어적·벤치마크"],
}).set_index("지표")
st.dataframe(summary_df, use_container_width=True)

# ── 인사이트 박스 ──────────────────────────────────────────────────────────────
st.divider()
st.subheader("💡 핵심 인사이트")
i1, i2, i3 = st.columns(3)
with i1:
    st.error("**개인: 구조적 불리**\n\n거래회전율 연 1,600%, 정보 비대칭, 처분효과(이익 빨리 실현·손실 오래 보유)로 시장 수익률 하회")
with i2:
    st.info("**외국인: 추세추종 우위**\n\n알고리즘·HFT 중심, 상승장에서 대규모 순매수. 하락 전환점에서 빠르게 매도 → 수익 방어")
with i3:
    st.success("**결론: '항상' 지진 않는다**\n\n하락장에서 개인의 역매수 타이밍이 적중하는 구간 존재. 문제는 과잉거래와 잘못된 종목 선택")