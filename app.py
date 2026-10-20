# Colors and chart styling
DARK_CHART_BG = "#111827"
DARK_GRID_COLOR = "#1f2937"
DARK_TEXT_COLOR = "#cbd5e1"
LEGEND_WHITE_TEXT = "#f8fafc"
CHART_HEIGHT = 255

day_window_data = df_day[(df_day.index >= t_start) & (df_day.index <= t_end)]
max_occ_day = max(day_window_data['occupancy_now'].max(), day_window_data['occupancy_forecast_15min'].max())
y_upper = max(8, int(max_occ_day) + 2) if pd.notna(max_occ_day) else 8

# ==============================================================================
# --- ROW 1: OCCUPANCY TIER (CARD & COMFORT ON LEFT | GRAPH ON RIGHT) ---
# ==============================================================================
row1_left, row1_right = st.columns([1.0, 1.48])

with row1_left:
    st.markdown("<div class='tier-header'>👥 Occupancy Status & Thermal Comfort</div>", unsafe_allow_html=True)
    sub_occ, sub_comf = st.columns([1.2, 0.88])
    if pred_occ > cur_occ:
        trend_symbol = "↑"
        trend_color = "#f87171"
    elif pred_occ < cur_occ:
        trend_symbol = "↓"
        trend_color = "#4ade80"
    else:
        trend_symbol = "="
        trend_color = "#60a5fa"

    with sub_occ:
        st.markdown(f"""
        <div class="metric-card-box" style="height: 255px;">
            <div class="card-top-title">👥 Headcount</div>
            <div style="display: flex; justify-content: space-around; align-items: center; text-align: center; margin: auto 0;">
                <div>
                    <div class="metric-label-muted">Current</div>
                    <div class="metric-main-val" style="font-size: 42px;">{cur_occ}</div>
                    <div class="metric-sub-unit">people</div>
                </div>
                <div style="border-left: 1.5px solid #2d3b55; height: 72px;"></div>
                <div>
                    <div class="metric-label-muted">15 min ahead</div>
                    <div class="metric-main-val" style="font-size: 42px;">
                        {pred_occ} 
                        <span style="font-size: 30px; font-weight: 900; color: {trend_color}; vertical-align: middle;">
                            {trend_symbol}
                        </span>
                    </div>
                    <div class="metric-sub-unit">people</div>
                </div>
            </div>
            <div style="height: 4px;"></div>
        </div>
        """, unsafe_allow_html=True)

    with sub_comf:
        is_comfort = (22.8 <= zone_temp <= 25.8)
        comfort_label = "COMFORTABLE" if is_comfort else "DEVIATION"
        comfort_icon = "😊" if is_comfort else "⚠️"
        bg_comfort = "linear-gradient(135deg, #15803d 0%, #166534 100%)" if is_comfort else "linear-gradient(135deg, #b45309 0%, #78350f 100%)"
        st.markdown(f"""
        <div class="comfort-card-box" style="background: {bg_comfort}; border: 1px solid {'#22c55e' if is_comfort else '#f59e0b'}; height: 255px;">
            <div style="font-size: 50px; line-height: 1.1; margin-bottom: 6px;">
                {comfort_icon}
            </div>
            <div>
                <div style="font-size: 12px; font-weight: 800; color: rgba(255,255,255,0.85); text-transform: uppercase; letter-spacing: 0.5px;">
                    Thermal Comfort
                </div>
                <div style="font-size: 20px; font-weight: 900; letter-spacing: 0.5px; line-height: 1.2; color: #ffffff;">
                    {comfort_label}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with row1_right:
    st.markdown("<div class='tier-header'>👥 Occupancy Tracking & 15 Min Forecast</div>", unsafe_allow_html=True)
    fig_occ = go.Figure()
    fig_occ.add_trace(go.Scatter(
        x=df_live.index, y=df_live['occupancy_forecast_15min'],
        mode='lines', name='15 Min Forecast',
        line=dict(color='#fb923c', width=2.8, dash='dash')
    ))
    fig_occ.add_trace(go.Scatter(
        x=df_live.index, y=df_live['occupancy_now'],
        mode='lines', name='Actual Occupancy',
        line=dict(color='#38bdf8', width=3.2)
    ))
    fig_occ.add_vline(x=datetime.combine(active_date, active_time), line_width=2, line_color="#ef4444")

    fig_occ.update_layout(
        height=CHART_HEIGHT,
        margin=dict(l=25, r=25, t=10, b=20),
        xaxis_title="", yaxis_title="People",
        plot_bgcolor=DARK_CHART_BG, paper_bgcolor=DARK_CHART_BG,
        font=dict(color=DARK_TEXT_COLOR, size=12),
        xaxis=dict(showgrid=True, gridcolor=DARK_GRID_COLOR, tickfont=dict(size=11, color=DARK_TEXT_COLOR), range=[t_start, t_end]),
        yaxis=dict(showgrid=True, gridcolor=DARK_GRID_COLOR, tickfont=dict(size=11, color=DARK_TEXT_COLOR), range=[0, y_upper], dtick=1),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=LEGEND_WHITE_TEXT),
            bgcolor="rgba(17, 24, 39, 0.85)",
            bordercolor="#374151",
            borderwidth=1
        )
    )
    st.plotly_chart(fig_occ, use_container_width=True)

st.markdown("<div style='margin-bottom: 22px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# --- ROW 2: TEMPERATURE TIER (CARD ON LEFT | GRAPH ON RIGHT) ---
# ==============================================================================
row2_left, row2_right = st.columns([1.0, 1.48])

with row2_left:
    st.markdown("<div class='tier-header'>🌡️ Temperature Metrics (°C)</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-card-box" style="height: 255px;">
        <div class="card-top-title">🌡️ Multi-Zone Telemetry</div>
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px; margin: auto 0;">
            <div class="temp-compartment">
                <div class="metric-label-muted" style="font-size: 13px; color: #94a3b8;">Zone</div>
                <div class="metric-main-val" style="color: #38bdf8; font-size: 38px;">{zone_temp:.1f}</div>
                <div class="metric-sub-unit" style="font-size: 12px; color: #64748b;">°C Actual</div>
            </div>
            <div class="temp-divider" style="height: 72px;"></div>
            <div class="temp-compartment">
                <div class="metric-label-muted" style="font-size: 13px; color: #94a3b8;">Setpoint</div>
                <div class="metric-main-val" style="color: #4ade80; font-size: 38px;">{setpoint_temp:.1f}</div>
                <div class="metric-sub-unit" style="font-size: 12px; color: #64748b;">°C Target</div>
            </div>
            <div class="temp-divider" style="height: 72px;"></div>
            <div class="temp-compartment">
                <div class="metric-label-muted" style="font-size: 13px; color: #94a3b8;">Outdoor</div>
                <div class="metric-main-val" style="color: #fb923c; font-size: 38px;">{outdoor_temp:.1f}</div>
                <div class="metric-sub-unit" style="font-size: 12px; color: #64748b;">°C Ambient</div>
            </div>
        </div>
        <div style="height: 4px;"></div>
    </div>
    """, unsafe_allow_html=True)

with row2_right:
    st.markdown("<div class='tier-header'>🌡️ Temperature Trend (°C)</div>", unsafe_allow_html=True)
    fig_temp = go.Figure()
    
    # Comfort band shading (22.8 - 25.8 °C)
    fig_temp.add_hrect(
        y0=22.8, y1=25.8, line_width=0, fillcolor="#22c55e", opacity=0.18,
        annotation_text="Comfort (22.8 - 25.8°C)", annotation_position="top right", annotation_font_size=11, annotation_font_color="#4ade80"
    )
    # Setpoint (24.0 °C)
    fig_temp.add_hline(
        y=24.0, line_dash="dash", line_color="#10b981", line_width=2, 
        annotation_text="Setpoint (24°C)", annotation_position="top left", annotation_font_size=11, annotation_font_color="#34d399"
    )
    # Zone Temperature
    fig_temp.add_trace(go.Scatter(
        x=df_live.index, y=df_live['predictive_room_temperature_C'],
        mode='lines', name='Zone Temp',
        line=dict(color='#38bdf8', width=3.2)
    ))
    # Outdoor Temperature
    fig_temp.add_trace(go.Scatter(
        x=df_live.index, y=df_live['outdoor_temperature_C'],
        mode='lines', name='Outdoor Temp',
        line=dict(color='#fb923c', width=2.4, dash='dot')
    ))
    fig_temp.add_vline(x=datetime.combine(active_date, active_time), line_width=2, line_color="#ef4444")

    fig_temp.update_layout(
        height=CHART_HEIGHT,
        margin=dict(l=25, r=25, t=10, b=20),
        xaxis_title="", yaxis_title="Temperature (°C)",
        plot_bgcolor=DARK_CHART_BG, paper_bgcolor=DARK_CHART_BG,
        font=dict(color=DARK_TEXT_COLOR, size=12),
        xaxis=dict(showgrid=True, gridcolor=DARK_GRID_COLOR, tickfont=dict(size=11, color=DARK_TEXT_COLOR), range=[t_start, t_end]),
        yaxis=dict(
            showgrid=True, 
            gridcolor=DARK_GRID_COLOR, 
            tickfont=dict(size=11, color=DARK_TEXT_COLOR),
            range=[22.0, 34.0],
            dtick=2.0
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=LEGEND_WHITE_TEXT),
            bgcolor="rgba(17, 24, 39, 0.85)",
            bordercolor="#374151",
            borderwidth=1
        )
    )
    st.plotly_chart(fig_temp, use_container_width=True)

st.markdown("<div style='margin-bottom: 22px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# --- ROW 3: ENERGY & POWER TIER (CARDS ON LEFT | GRAPH ON RIGHT) ---
# ==============================================================================
row3_left, row3_right = st.columns([1.0, 1.48])

with row3_left:
    st.markdown("<div class='tier-header'>⚡ Power Demand & Cumulative Energy</div>", unsafe_allow_html=True)
    sub_pwr, sub_egy = st.columns([0.82, 1.38])
    
    # Current Power Card
    with sub_pwr:
        st.markdown(f"""
        <div class="metric-card-box" style="height: 255px;">
            <div class="card-top-title">⚡ Instant Load</div>
            <div style="text-align: center; margin: auto 0; background-color: #162032; border: 1.5px solid #2d3b55; border-radius: 14px; padding: 16px 8px;">
                <div class="metric-label-muted" style="font-size: 12px; color: #94a3b8;">Active Demand</div>
                <div class="metric-main-val" style="color: #38bdf8; font-size: 38px; margin: 6px 0;">
                    {cur_power:.2f}
                </div>
                <div class="metric-sub-unit" style="font-size: 13px; font-weight: 800; color: #64748b;">kW active load</div>
            </div>
            <div style="height: 4px;"></div>
        </div>
        """, unsafe_allow_html=True)

    # Daily Energy Usage Card
    with sub_egy:
        st.markdown(f"""
        <div class="metric-card-box" style="height: 255px;">
            <div class="card-top-title">{card_title}</div>
            <div class="gauge-container" style="padding: 0 4px; margin: auto 0;">
                <div style="display: flex; flex-direction: column; justify-content: center; gap: 10px; flex: 1;">
                    <div style="background-color: #162032; border: 1.5px solid #2d3b55; border-radius: 12px; padding: 10px 12px;">
                        <div class="metric-label-muted" style="font-size: 11px;">Predictive HVAC</div>
                        <div style="font-size: 26px; font-weight: 900; color: #60a5fa; line-height: 1.05;">
                            {disp_pred:.2f} <span style="font-size: 12.5px; font-weight: 700; color: #94a3b8;">kWh</span>
                        </div>
                    </div>
                    <div style="background-color: #162032; border: 1.5px solid #2d3b55; border-radius: 12px; padding: 10px 12px;">
                        <div class="metric-label-muted" style="font-size: 11px;">Scheduled Baseline</div>
                        <div style="font-size: 26px; font-weight: 900; color: #fb923c; line-height: 1.05;">
                            {disp_sched:.2f} <span style="font-size: 12.5px; font-weight: 700; color: #94a3b8;">kWh</span>
                        </div>
                    </div>
                </div>
                <div class="circular-gauge" style="background: conic-gradient(#22c55e 0deg {gauge_deg}deg, #1e293b {gauge_deg}deg 360deg);">
                    <div class="circular-gauge-inner">
                        <div style="font-size: 10px; font-weight: 900; color: #4ade80; text-transform: uppercase; letter-spacing: 0.8px;">SAVING</div>
                        <div style="font-size: 28px; font-weight: 900; color: #f8fafc; line-height: 1.05;">{disp_pct:.1f}%</div>
                        <div style="font-size: 11px; font-weight: 700; color: #94a3b8; margin-top: 2px;">-{disp_saved:.2f} kWh</div>
                    </div>
                </div>
            </div>
            <div style="height: 4px;"></div>
        </div>
        """, unsafe_allow_html=True)
