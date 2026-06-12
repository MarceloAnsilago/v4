from flask import Flask, Response, redirect, render_template, request, url_for


GROUP_1_FIELDS = [
    {
        "name": "m_magic",
        "label": "Magic Number (ID)",
        "kind": "number",
        "input_type": "number",
        "default": "1780952729",
        "help": "Identificador unico do robo no ativo.",
    },
    {
        "name": "m_processo",
        "label": "Modo de processamento",
        "kind": "select",
        "default": "es_tick",
        "options": [
            ("es_tick", "Cada tick"),
            ("es_seg", "Cada segundo"),
        ],
        "help": "Corresponde ao enum e_pro do EA.",
    },
    {
        "name": "m_mercado",
        "label": "Tipo de mercado",
        "kind": "select",
        "default": "(e_mercado)ORDER_FILLING_RETURN",
        "options": [
            ("(e_mercado)ORDER_FILLING_RETURN", "B3"),
            ("(e_mercado)ORDER_FILLING_FOK", "Forex"),
        ],
        "help": "Corresponde ao enum e_mercado do EA.",
    },
    {
        "name": "m_validade",
        "label": "Modo operacional",
        "kind": "select",
        "default": "(e_validade)ORDER_TIME_GTC",
        "options": [
            ("(e_validade)ORDER_TIME_GTC", "Swing Trade"),
            ("(e_validade)ORDER_TIME_DAY", "Day Trade"),
        ],
        "help": "Corresponde ao enum e_validade do EA.",
    },
]

GROUP_1_FLOW_FIELDS = [
    {
        "name": "operar_compra",
        "label": "Deseja operar na compra",
        "default": "sim",
        "options": [("sim", "Sim"), ("nao", "Nao")],
        "help": "Se desabilitar, o fluxo pode pular configuracoes de sinais de compra.",
    },
    {
        "name": "operar_venda",
        "label": "Deseja operar na venda",
        "default": "sim",
        "options": [("sim", "Sim"), ("nao", "Nao")],
        "help": "Se desabilitar, o fluxo pode pular configuracoes de sinais de venda.",
    },
]

GROUP_2_FIELDS = [
    {
        "name": "m_timeframe",
        "label": "Tempo grafico principal",
        "kind": "select",
        "default": "PERIOD_CURRENT",
        "options": [
            ("PERIOD_CURRENT", "Corrente"),
            ("PERIOD_M1", "M1"),
            ("PERIOD_M2", "M2"),
            ("PERIOD_M3", "M3"),
            ("PERIOD_M4", "M4"),
            ("PERIOD_M5", "M5"),
            ("PERIOD_M6", "M6"),
            ("PERIOD_M10", "M10"),
            ("PERIOD_M12", "M12"),
            ("PERIOD_M15", "M15"),
            ("PERIOD_M30", "M30"),
            ("PERIOD_H1", "H1"),
            ("PERIOD_H2", "H2"),
            ("PERIOD_H3", "H3"),
            ("PERIOD_H4", "H4"),
            ("PERIOD_H6", "H6"),
            ("PERIOD_H8", "H8"),
            ("PERIOD_H12", "H12"),
            ("PERIOD_D1", "D1"),
            ("PERIOD_W1", "W1"),
            ("PERIOD_MN1", "MN1"),
        ],
        "help": "Corresponde ao ENUM_TIMEFRAMES do EA.",
    },
    {
        "name": "m_volume",
        "label": "Volume inicial",
        "kind": "number",
        "input_type": "number",
        "default": "100",
        "help": "Volume inicial definido no grupo CONFIGURACAO ADICIONAL.",
    },
    {
        "name": "m_spread",
        "label": "Spread maximo",
        "kind": "number",
        "input_type": "number",
        "default": "0",
        "help": "Spread maximo permitido em pontos.",
    },
]

PRICE_OPTIONS = [
    ("es_mercado", "Preco atual"),
    ("es_max", "Maxima atual"),
    ("es_min", "Minima atual"),
    ("es_open", "Abertura atual"),
    ("es_last_max", "Maxima anterior"),
    ("es_last_min", "Minima anterior"),
    ("es_close", "Fechamento anterior"),
    ("es_3_max", "Maxima dos 3 ultimos"),
    ("es_3_min", "Minima dos 3 ultimos"),
    ("es_day_max", "Maxima do dia"),
    ("es_day_min", "Minima do dia"),
    ("es_day_open", "Abertura do dia"),
    ("es_day_last_max", "Maxima dia anterior"),
    ("es_day_last_min", "Minima dia anterior"),
    ("es_day_last_close", "Fechamento dia anterior"),
    ("es_bid", "Melhor comprador"),
    ("es_ask", "Melhor vendedor"),
]

TIME_OPTIONS = [
    ("es_s", "Segundos"),
    ("es_m", "Minutos"),
    ("es_h", "Horas"),
    ("es_v", "Velas"),
]

HOUR_OPTIONS = [(str(hour), f"{hour:02d}") for hour in range(24)]
MINUTE_OPTIONS = [(str(minute), f"{minute:02d}") for minute in range(60)]
WEEKDAY_OPTIONS = [
    ("es_diariamente", "Diariamente"),
    ("es_segunda", "Segunda"),
    ("es_terca", "Terca"),
    ("es_quarta", "Quarta"),
    ("es_quinta", "Quinta"),
    ("es_sexta", "Sexta"),
    ("es_sabado", "Sabado"),
]

GROUP_3_FIELDS = [
    {
        "name": "m_pendente_in",
        "label": "Ordem de entrada",
        "kind": "select",
        "default": "es_sim",
        "options": [("es_nao", "A mercado"), ("es_sim", "Pendente")],
    },
    {
        "name": "m_cancel_in",
        "label": "Expiracao da ordem",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_dis_in",
        "label": "Distancia das ordens",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_price_buy",
        "label": "Entrada na compra",
        "kind": "select",
        "default": "es_mercado",
        "options": PRICE_OPTIONS,
    },
    {
        "name": "m_price_sell",
        "label": "Entrada na venda",
        "kind": "select",
        "default": "es_mercado",
        "options": PRICE_OPTIONS,
    },
    {
        "name": "m_pendente_out",
        "label": "Ordem de saida",
        "kind": "select",
        "default": "es_sim",
        "options": [("es_nao", "A mercado"), ("es_sim", "Pendente")],
    },
    {
        "name": "m_cancel_out",
        "label": "Expiracao da ordem",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_dis_out",
        "label": "Distancia da saida",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_price_out_buy",
        "label": "Saida da compra",
        "kind": "select",
        "default": "es_mercado",
        "options": PRICE_OPTIONS,
    },
    {
        "name": "m_price_out_sell",
        "label": "Saida da venda",
        "kind": "select",
        "default": "es_mercado",
        "options": PRICE_OPTIONS,
    },
]

GROUP_4_FIELDS = [
    {
        "name": "m_alvos_sl2",
        "label": "Usar stop personalizado",
        "kind": "select",
        "default": "es_sim",
        "options": [("es_nao", "Nao"), ("es_sim", "Sim")],
    },
    {
        "name": "m_dis_sl2",
        "label": "Distancia ordem stop",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_price_sl2_buy",
        "label": "Stoploss da compra",
        "kind": "select",
        "default": "es_mercado",
        "options": PRICE_OPTIONS,
    },
    {
        "name": "m_price_sl2_sell",
        "label": "Stoploss da venda",
        "kind": "select",
        "default": "es_mercado",
        "options": PRICE_OPTIONS,
    },
    {
        "name": "m_alvos_tp2",
        "label": "Usar take personalizado",
        "kind": "select",
        "default": "es_sim",
        "options": [("es_nao", "Nao"), ("es_sim", "Sim")],
    },
    {
        "name": "m_dis_tp2",
        "label": "Distancia ordem take",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_price_tp2_buy",
        "label": "Takeprofit da compra",
        "kind": "select",
        "default": "es_mercado",
        "options": PRICE_OPTIONS,
    },
    {
        "name": "m_price_tp2_sell",
        "label": "Takeprofit da venda",
        "kind": "select",
        "default": "es_mercado",
        "options": PRICE_OPTIONS,
    },
]

GROUP_5_FIELDS = [
    {
        "name": "m_sl",
        "label": "Stoploss inicial",
        "kind": "number",
        "input_type": "number",
        "default": "450",
    },
    {
        "name": "m_sl_be",
        "label": "Inicio do Break Even SL",
        "kind": "number",
        "input_type": "number",
        "default": "450",
    },
    {
        "name": "m_sl_be_dis",
        "label": "Distancia do Break Even SL",
        "kind": "number",
        "input_type": "number",
        "default": "5",
    },
    {
        "name": "m_sl_ts",
        "label": "Inicio do Trailling Stop",
        "kind": "number",
        "input_type": "number",
        "default": "450",
    },
    {
        "name": "m_sl_ts_step",
        "label": "Passo do Trailling Stop",
        "kind": "number",
        "input_type": "number",
        "default": "5",
    },
]

GROUP_6_FIELDS = [
    {
        "name": "m_tp",
        "label": "Takeprofit inicial",
        "kind": "number",
        "input_type": "number",
        "default": "800",
    },
    {
        "name": "m_tp_be",
        "label": "Inicio do Break Even TP",
        "kind": "number",
        "input_type": "number",
        "default": "400",
    },
    {
        "name": "m_tp_be_dis",
        "label": "Distancia do Break Even TP",
        "kind": "number",
        "input_type": "number",
        "default": "5",
    },
    {
        "name": "m_tp_ts",
        "label": "Inicio do Trailling Profit",
        "kind": "number",
        "input_type": "number",
        "default": "505",
    },
    {
        "name": "m_tp_ts_step",
        "label": "Passo do Trailling Profit",
        "kind": "number",
        "input_type": "number",
        "default": "5",
    },
]

GROUP_7_FIELDS = [
    {
        "name": "m_temporal_ref",
        "label": "Referencia de tempo",
        "kind": "select",
        "default": "es_s",
        "options": TIME_OPTIONS,
    },
    {
        "name": "m_temporal_pos_time",
        "label": "Tempo de saida",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_temporal_pos_max",
        "label": "Saldo maximo",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_temporal_pos_min",
        "label": "Saldo minimo",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_temporal_neg_time",
        "label": "Tempo de saida",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_temporal_neg_max",
        "label": "Saldo maximo",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_temporal_neg_min",
        "label": "Saldo minimo",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
]

GROUP_8_FIELDS = [
    {
        "name": "m_espera_ref",
        "label": "Referencia de tempo",
        "kind": "select",
        "default": "es_s",
        "options": TIME_OPTIONS,
    },
    {
        "name": "m_espera_in",
        "label": "Tempo para nova entrada",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_espera_out",
        "label": "Tempo minimo de posicao",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
]

GROUP_9_FIELDS = [
    {
        "name": "m_zerar",
        "label": "Deseja zerar por horario",
        "kind": "select",
        "default": "es_sim",
        "options": [("es_nao", "Nao"), ("es_sim", "Sim")],
    },
    {
        "name": "m_hr_inicio",
        "label": "Horario inicial das operacoes",
        "kind": "select",
        "default": "9",
        "options": HOUR_OPTIONS,
    },
    {
        "name": "m_min_inicio",
        "label": "Minuto inicial das operacoes",
        "kind": "select",
        "default": "33",
        "options": MINUTE_OPTIONS,
    },
    {
        "name": "m_hr_final",
        "label": "Horario final das operacoes",
        "kind": "select",
        "default": "16",
        "options": HOUR_OPTIONS,
    },
    {
        "name": "m_min_final",
        "label": "Minuto final das operacoes",
        "kind": "select",
        "default": "30",
        "options": MINUTE_OPTIONS,
    },
    {
        "name": "m_hr_zerar",
        "label": "Horario de zerar as operacoes",
        "kind": "select",
        "default": "17",
        "options": HOUR_OPTIONS,
    },
    {
        "name": "m_min_zerar",
        "label": "Minuto de zerar as operacoes",
        "kind": "select",
        "default": "0",
        "options": MINUTE_OPTIONS,
    },
]

GROUP_10_FIELDS = [
    {
        "name": "m_pausa_ref",
        "label": "Referencia de tempo",
        "kind": "select",
        "default": "es_s",
        "options": TIME_OPTIONS,
    },
    {
        "name": "m_pausa_1_hr",
        "label": "Hora pausa 1",
        "kind": "select",
        "default": "0",
        "options": HOUR_OPTIONS,
    },
    {
        "name": "m_pausa_1_min",
        "label": "Minuto pausa 1",
        "kind": "select",
        "default": "0",
        "options": MINUTE_OPTIONS,
    },
    {
        "name": "m_pausa_1_dia",
        "label": "Dia da pausa 1",
        "kind": "select",
        "default": "es_diariamente",
        "options": WEEKDAY_OPTIONS,
    },
    {
        "name": "m_pausa_1_tempo",
        "label": "Duracao da pausa 1",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_pausa_2_hr",
        "label": "Hora pausa 2",
        "kind": "select",
        "default": "0",
        "options": HOUR_OPTIONS,
    },
    {
        "name": "m_pausa_2_min",
        "label": "Minuto pausa 2",
        "kind": "select",
        "default": "0",
        "options": MINUTE_OPTIONS,
    },
    {
        "name": "m_pausa_2_dia",
        "label": "Dia da pausa 2",
        "kind": "select",
        "default": "es_diariamente",
        "options": WEEKDAY_OPTIONS,
    },
    {
        "name": "m_pausa_2_tempo",
        "label": "Duracao da pausa 2",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
]

GROUP_11_FIELDS = [
    {
        "name": "m_ac1_dis",
        "label": "Distancia contra 1",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_ac1_lot",
        "label": "Volume contra 1",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_ac2_dis",
        "label": "Distancia contra 2",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_ac2_lot",
        "label": "Volume contra 2",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_ac3_dis",
        "label": "Distancia contra 3",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_ac3_lot",
        "label": "Volume contra 3",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_ac4_dis",
        "label": "Distancia contra 4",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_ac4_lot",
        "label": "Volume contra 4",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_ac5_dis",
        "label": "Distancia contra 5",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_ac5_lot",
        "label": "Volume contra 5",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
]

GROUP_12_FIELDS = [
    {
        "name": "m_af1_dis",
        "label": "Distancia a favor 1",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_af1_lot",
        "label": "Volume a favor 1",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_af2_dis",
        "label": "Distancia a favor 2",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_af2_lot",
        "label": "Volume a favor 2",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_af3_dis",
        "label": "Distancia a favor 3",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_af3_lot",
        "label": "Volume a favor 3",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_af4_dis",
        "label": "Distancia a favor 4",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_af4_lot",
        "label": "Volume a favor 4",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_af5_dis",
        "label": "Distancia a favor 5",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_af5_lot",
        "label": "Volume a favor 5",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
]

GROUP_13_FIELDS = [
    {
        "name": "m_pendente_parcial",
        "label": "Ordem pendente para parcial",
        "kind": "select",
        "default": "es_sim",
        "options": [("es_nao", "Nao"), ("es_sim", "Sim")],
    },
    {
        "name": "m_p1_dis",
        "label": "Distancia parcial 1",
        "kind": "number",
        "input_type": "number",
        "default": "200",
    },
    {
        "name": "m_p1_lot",
        "label": "Volume parcial 1",
        "kind": "number",
        "input_type": "number",
        "default": "100",
    },
    {
        "name": "m_p2_dis",
        "label": "Distancia parcial 2",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_p2_lot",
        "label": "Volume parcial 2",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_p3_dis",
        "label": "Distancia parcial 3",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_p3_lot",
        "label": "Volume parcial 3",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_p4_dis",
        "label": "Distancia parcial 4",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
    {
        "name": "m_p4_lot",
        "label": "Volume parcial 4",
        "kind": "number",
        "input_type": "number",
        "default": "0",
    },
]

GROUP_14_FIELDS = [
    {
        "name": "m_grad_qtd",
        "label": "Quantidade de niveis",
        "kind": "number",
        "input_type": "number",
        "default": "5",
    },
    {
        "name": "m_grad_vol",
        "label": "Volume das ordens",
        "kind": "number",
        "input_type": "number",
        "default": "100",
    },
    {
        "name": "m_grad_max",
        "label": "Limite de entradas",
        "kind": "number",
        "input_type": "number",
        "default": "5",
    },
    {
        "name": "m_gra_dis",
        "label": "Distancia dos niveis",
        "kind": "number",
        "input_type": "number",
        "default": "100",
    },
    {
        "name": "m_gra_tp",
        "label": "Alvo parcial",
        "kind": "number",
        "input_type": "number",
        "default": "100",
    },
    {
        "name": "m_pendente_grad",
        "label": "Ordem pendente para parcial do gradiente",
        "kind": "select",
        "default": "es_sim",
        "options": [("es_nao", "Nao"), ("es_sim", "Sim")],
    },
    {
        "name": "m_grad_ajuste",
        "label": "Reposicionar ordem",
        "kind": "number",
        "input_type": "number",
        "default": "100",
    },
    {
        "name": "m_grad_repo",
        "label": "Reposicionar todos os niveis",
        "kind": "select",
        "default": "es_sim",
        "options": [("es_nao", "Nao"), ("es_sim", "Sim")],
    },
]


def sanitize_robot_name(raw_value: str | None) -> str:
    if not raw_value:
        return "MeuRobo"

    cleaned = "".join(ch for ch in raw_value.strip() if ch.isalnum() or ch in ("_", "-"))
    return cleaned or "MeuRobo"


def build_group_1_values(form_data=None):
    values = {}
    for field in GROUP_1_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_1_flow_values(form_data=None):
    values = {}
    for field in GROUP_1_FLOW_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_2_values(form_data=None):
    values = {}
    for field in GROUP_2_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_3_values(form_data=None):
    values = {}
    for field in GROUP_3_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_4_values(form_data=None):
    values = {}
    for field in GROUP_4_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_5_values(form_data=None):
    values = {}
    for field in GROUP_5_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_6_values(form_data=None):
    values = {}
    for field in GROUP_6_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_7_values(form_data=None):
    values = {}
    for field in GROUP_7_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_8_values(form_data=None):
    values = {}
    for field in GROUP_8_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_9_values(form_data=None):
    values = {}
    for field in GROUP_9_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_10_values(form_data=None):
    values = {}
    for field in GROUP_10_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_11_values(form_data=None):
    values = {}
    for field in GROUP_11_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_12_values(form_data=None):
    values = {}
    for field in GROUP_12_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_13_values(form_data=None):
    values = {}
    for field in GROUP_13_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def build_group_14_values(form_data=None):
    values = {}
    for field in GROUP_14_FIELDS:
        default_value = field["default"]
        values[field["name"]] = form_data.get(field["name"], default_value) if form_data else default_value
    return values


def sanitize_calc_mode(raw_value):
    return raw_value if raw_value in ("pts", "pct") else "pts"


def build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, setup_name: str, group_8_values=None, group_9_values=None, group_10_values=None, group_11_values=None, group_12_values=None, group_13_values=None, group_14_values=None):
    if group_8_values is None:
        group_8_values = build_group_8_values()
    if group_9_values is None:
        group_9_values = build_group_9_values()
    if group_10_values is None:
        group_10_values = build_group_10_values()
    if group_11_values is None:
        group_11_values = build_group_11_values()
    if group_12_values is None:
        group_12_values = build_group_12_values()
    if group_13_values is None:
        group_13_values = build_group_13_values()
    if group_14_values is None:
        group_14_values = build_group_14_values()
    return "\n".join(
        [
            "; Grupo 1 - Parametrizacao Inicial",
            f"m_set={setup_name}",
            f"m_magic={group_1_values['m_magic']}",
            f"m_processo={group_1_values['m_processo']}",
            f"m_mercado={group_1_values['m_mercado']}",
            f"m_validade={group_1_values['m_validade']}",
            "",
            "; Grupo 2 - Configuracao Adicional",
            f"m_timeframe={group_2_values['m_timeframe']}",
            f"m_volume={group_2_values['m_volume']}",
            f"m_spread={group_2_values['m_spread']}",
            "",
            "; Grupo 3 - Tipo de Ordens",
            f"m_pendente_in={group_3_values['m_pendente_in']}",
            f"m_cancel_in={group_3_values['m_cancel_in']}",
            f"m_dis_in={group_3_values['m_dis_in']}",
            f"m_price_buy={group_3_values['m_price_buy']}",
            f"m_price_sell={group_3_values['m_price_sell']}",
            f"m_pendente_out={group_3_values['m_pendente_out']}",
            f"m_cancel_out={group_3_values['m_cancel_out']}",
            f"m_dis_out={group_3_values['m_dis_out']}",
            f"m_price_out_buy={group_3_values['m_price_out_buy']}",
            f"m_price_out_sell={group_3_values['m_price_out_sell']}",
            "",
            "; Grupo 4 - Alvos Personalizados",
            f"m_alvos_sl2={group_4_values['m_alvos_sl2']}",
            f"m_dis_sl2={group_4_values['m_dis_sl2']}",
            f"m_price_sl2_buy={group_4_values['m_price_sl2_buy']}",
            f"m_price_sl2_sell={group_4_values['m_price_sl2_sell']}",
            f"m_alvos_tp2={group_4_values['m_alvos_tp2']}",
            f"m_dis_tp2={group_4_values['m_dis_tp2']}",
            f"m_price_tp2_buy={group_4_values['m_price_tp2_buy']}",
            f"m_price_tp2_sell={group_4_values['m_price_tp2_sell']}",
            "",
            "; Grupo 5 - Stoploss",
            f"m_sl={group_5_values['m_sl']}",
            f"m_sl_be={group_5_values['m_sl_be']}",
            f"m_sl_be_dis={group_5_values['m_sl_be_dis']}",
            f"m_sl_ts={group_5_values['m_sl_ts']}",
            f"m_sl_ts_step={group_5_values['m_sl_ts_step']}",
            "",
            "; Grupo 6 - Take Profit",
            f"m_tp={group_6_values['m_tp']}",
            f"m_tp_be={group_6_values['m_tp_be']}",
            f"m_tp_be_dis={group_6_values['m_tp_be_dis']}",
            f"m_tp_ts={group_6_values['m_tp_ts']}",
            f"m_tp_ts_step={group_6_values['m_tp_ts_step']}",
            "",
            "; Grupo 7 - Saida Temporal",
            f"m_temporal_ref={group_7_values['m_temporal_ref']}",
            f"m_temporal_pos_time={group_7_values['m_temporal_pos_time']}",
            f"m_temporal_pos_max={group_7_values['m_temporal_pos_max']}",
            f"m_temporal_pos_min={group_7_values['m_temporal_pos_min']}",
            f"m_temporal_neg_time={group_7_values['m_temporal_neg_time']}",
            f"m_temporal_neg_max={group_7_values['m_temporal_neg_max']}",
            f"m_temporal_neg_min={group_7_values['m_temporal_neg_min']}",
            "",
            "; Grupo 8 - Filtro de Tempo",
            f"m_espera_ref={group_8_values['m_espera_ref']}",
            f"m_espera_in={group_8_values['m_espera_in']}",
            f"m_espera_out={group_8_values['m_espera_out']}",
            "",
            "; Grupo 9 - Horarios",
            f"m_hr_inicio={group_9_values['m_hr_inicio']}",
            f"m_min_inicio={group_9_values['m_min_inicio']}",
            f"m_hr_final={group_9_values['m_hr_final']}",
            f"m_min_final={group_9_values['m_min_final']}",
            f"m_zerar={group_9_values['m_zerar']}",
            f"m_hr_zerar={group_9_values['m_hr_zerar']}",
            f"m_min_zerar={group_9_values['m_min_zerar']}",
            "",
            "; Grupo 10 - Pausas Operacionais",
            f"m_pausa_ref={group_10_values['m_pausa_ref']}",
            f"m_pausa_1_hr={group_10_values['m_pausa_1_hr']}",
            f"m_pausa_1_min={group_10_values['m_pausa_1_min']}",
            f"m_pausa_1_dia={group_10_values['m_pausa_1_dia']}",
            f"m_pausa_1_tempo={group_10_values['m_pausa_1_tempo']}",
            f"m_pausa_2_hr={group_10_values['m_pausa_2_hr']}",
            f"m_pausa_2_min={group_10_values['m_pausa_2_min']}",
            f"m_pausa_2_dia={group_10_values['m_pausa_2_dia']}",
            f"m_pausa_2_tempo={group_10_values['m_pausa_2_tempo']}",
            "",
            "; Grupo 11 - Aumento Contra",
            f"m_ac1_dis={group_11_values['m_ac1_dis']}",
            f"m_ac1_lot={group_11_values['m_ac1_lot']}",
            f"m_ac2_dis={group_11_values['m_ac2_dis']}",
            f"m_ac2_lot={group_11_values['m_ac2_lot']}",
            f"m_ac3_dis={group_11_values['m_ac3_dis']}",
            f"m_ac3_lot={group_11_values['m_ac3_lot']}",
            f"m_ac4_dis={group_11_values['m_ac4_dis']}",
            f"m_ac4_lot={group_11_values['m_ac4_lot']}",
            f"m_ac5_dis={group_11_values['m_ac5_dis']}",
            f"m_ac5_lot={group_11_values['m_ac5_lot']}",
            "",
            "; Grupo 12 - Aumento A Favor",
            f"m_af1_dis={group_12_values['m_af1_dis']}",
            f"m_af1_lot={group_12_values['m_af1_lot']}",
            f"m_af2_dis={group_12_values['m_af2_dis']}",
            f"m_af2_lot={group_12_values['m_af2_lot']}",
            f"m_af3_dis={group_12_values['m_af3_dis']}",
            f"m_af3_lot={group_12_values['m_af3_lot']}",
            f"m_af4_dis={group_12_values['m_af4_dis']}",
            f"m_af4_lot={group_12_values['m_af4_lot']}",
            f"m_af5_dis={group_12_values['m_af5_dis']}",
            f"m_af5_lot={group_12_values['m_af5_lot']}",
            "",
            "; Grupo 13 - Saidas Parciais",
            f"m_pendente_parcial={group_13_values['m_pendente_parcial']}",
            f"m_p1_dis={group_13_values['m_p1_dis']}",
            f"m_p1_lot={group_13_values['m_p1_lot']}",
            f"m_p2_dis={group_13_values['m_p2_dis']}",
            f"m_p2_lot={group_13_values['m_p2_lot']}",
            f"m_p3_dis={group_13_values['m_p3_dis']}",
            f"m_p3_lot={group_13_values['m_p3_lot']}",
            f"m_p4_dis={group_13_values['m_p4_dis']}",
            f"m_p4_lot={group_13_values['m_p4_lot']}",
            "",
            "; Grupo 14 - Gradiente Linear",
            f"m_grad_qtd={group_14_values['m_grad_qtd']}",
            f"m_grad_vol={group_14_values['m_grad_vol']}",
            f"m_grad_max={group_14_values['m_grad_max']}",
            f"m_gra_dis={group_14_values['m_gra_dis']}",
            f"m_gra_tp={group_14_values['m_gra_tp']}",
            f"m_pendente_grad={group_14_values['m_pendente_grad']}",
            f"m_grad_ajuste={group_14_values['m_grad_ajuste']}",
            f"m_grad_repo={group_14_values['m_grad_repo']}",
        ]
    )


app = Flask(__name__)


@app.route("/")
def index():
    robot_name = sanitize_robot_name(request.args.get("robot"))
    group_1_values = build_group_1_values(request.args)
    group_2_values = build_group_2_values(request.args)
    group_3_values = build_group_3_values(request.args)
    group_4_values = build_group_4_values(request.args)
    group_5_values = build_group_5_values(request.args)
    group_6_values = build_group_6_values(request.args)
    group_7_values = build_group_7_values(request.args)
    group_8_values = build_group_8_values(request.args)
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name, group_8_values)
    return render_template("index.html", robot_name=robot_name, values=group_1_values, group_2_values=group_2_values, group_3_values=group_3_values, group_4_values=group_4_values, group_5_values=group_5_values, group_6_values=group_6_values, group_7_values=group_7_values, group_8_values=group_8_values, set_content=set_content)


@app.route("/iniciar", methods=["POST"])
def iniciar():
    robot_name = sanitize_robot_name(request.form.get("robot_name"))
    group_1_values = build_group_1_values(request.form)
    group_2_values = build_group_2_values(request.form)
    group_3_values = build_group_3_values(request.form)
    group_4_values = build_group_4_values(request.form)
    group_5_values = build_group_5_values(request.form)
    group_6_values = build_group_6_values(request.form)
    group_7_values = build_group_7_values(request.form)
    group_8_values = build_group_8_values(request.form)
    return redirect(
        url_for(
            "grupo_1",
            robot=robot_name,
            m_magic=group_1_values["m_magic"],
            m_processo=group_1_values["m_processo"],
            m_mercado=group_1_values["m_mercado"],
            m_validade=group_1_values["m_validade"],
            m_timeframe=group_2_values["m_timeframe"],
            m_volume=group_2_values["m_volume"],
            m_spread=group_2_values["m_spread"],
            m_pendente_in=group_3_values["m_pendente_in"],
            m_cancel_in=group_3_values["m_cancel_in"],
            m_dis_in=group_3_values["m_dis_in"],
            m_price_buy=group_3_values["m_price_buy"],
            m_price_sell=group_3_values["m_price_sell"],
            m_pendente_out=group_3_values["m_pendente_out"],
            m_cancel_out=group_3_values["m_cancel_out"],
            m_dis_out=group_3_values["m_dis_out"],
            m_price_out_buy=group_3_values["m_price_out_buy"],
            m_price_out_sell=group_3_values["m_price_out_sell"],
            m_alvos_sl2=group_4_values["m_alvos_sl2"],
            m_dis_sl2=group_4_values["m_dis_sl2"],
            m_price_sl2_buy=group_4_values["m_price_sl2_buy"],
            m_price_sl2_sell=group_4_values["m_price_sl2_sell"],
            m_alvos_tp2=group_4_values["m_alvos_tp2"],
            m_dis_tp2=group_4_values["m_dis_tp2"],
            m_price_tp2_buy=group_4_values["m_price_tp2_buy"],
            m_price_tp2_sell=group_4_values["m_price_tp2_sell"],
            m_sl=group_5_values["m_sl"],
            m_sl_be=group_5_values["m_sl_be"],
            m_sl_be_dis=group_5_values["m_sl_be_dis"],
            m_sl_ts=group_5_values["m_sl_ts"],
            m_sl_ts_step=group_5_values["m_sl_ts_step"],
            m_tp=group_6_values["m_tp"],
            m_tp_be=group_6_values["m_tp_be"],
            m_tp_be_dis=group_6_values["m_tp_be_dis"],
            m_tp_ts=group_6_values["m_tp_ts"],
            m_tp_ts_step=group_6_values["m_tp_ts_step"],
            m_temporal_ref=group_7_values["m_temporal_ref"],
            m_temporal_pos_time=group_7_values["m_temporal_pos_time"],
            m_temporal_pos_max=group_7_values["m_temporal_pos_max"],
            m_temporal_pos_min=group_7_values["m_temporal_pos_min"],
            m_temporal_neg_time=group_7_values["m_temporal_neg_time"],
            m_temporal_neg_max=group_7_values["m_temporal_neg_max"],
            m_temporal_neg_min=group_7_values["m_temporal_neg_min"],
            m_espera_ref=group_8_values["m_espera_ref"],
            m_espera_in=group_8_values["m_espera_in"],
            m_espera_out=group_8_values["m_espera_out"],
        )
    )


@app.route("/grupo-1", methods=["GET", "POST"])
def grupo_1():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    flow_values = build_group_1_flow_values(source_data)
    set_content = build_set_content(values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_1.html",
        fields=GROUP_1_FIELDS,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        flow_fields=GROUP_1_FLOW_FIELDS,
        flow_values=flow_values,
        values=values,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-2", methods=["GET", "POST"])
def grupo_2():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_2.html",
        group_1_values=group_1_values,
        fields=GROUP_2_FIELDS,
        values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-3", methods=["GET", "POST"])
def grupo_3():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_3.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        fields=GROUP_3_FIELDS,
        values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        calc_mode=calc_mode,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-4", methods=["GET", "POST"])
def grupo_4():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_4.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        fields=GROUP_4_FIELDS,
        values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        calc_mode=calc_mode,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-5", methods=["GET", "POST"])
def grupo_5():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_5.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        fields=GROUP_5_FIELDS,
        values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        calc_mode=calc_mode,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-6", methods=["GET", "POST"])
def grupo_6():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_6.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        fields=GROUP_6_FIELDS,
        values=group_6_values,
        group_7_values=group_7_values,
        calc_mode=calc_mode,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-7", methods=["GET", "POST"])
def grupo_7():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    group_8_values = build_group_8_values(source_data)
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name, group_8_values)
    started = request.method == "POST"
    return render_template(
        "grupo_7.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        fields=GROUP_7_FIELDS,
        values=group_7_values,
        group_8_values=group_8_values,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-8", methods=["GET", "POST"])
def grupo_8():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    group_8_values = build_group_8_values(source_data)
    group_9_values = build_group_9_values(source_data)
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name, group_8_values, group_9_values)
    started = request.method == "POST"
    return render_template(
        "grupo_8.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        fields=GROUP_8_FIELDS,
        values=group_8_values,
        group_9_values=group_9_values,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-9", methods=["GET", "POST"])
def grupo_9():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    group_8_values = build_group_8_values(source_data)
    group_9_values = build_group_9_values(source_data)
    group_10_values = build_group_10_values(source_data)
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name, group_8_values, group_9_values, group_10_values)
    started = request.method == "POST"
    return render_template(
        "grupo_9.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        group_8_values=group_8_values,
        group_10_values=group_10_values,
        fields=GROUP_9_FIELDS,
        values=group_9_values,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-10", methods=["GET", "POST"])
def grupo_10():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    group_8_values = build_group_8_values(source_data)
    group_9_values = build_group_9_values(source_data)
    group_10_values = build_group_10_values(source_data)
    group_11_values = build_group_11_values(source_data)
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name, group_8_values, group_9_values, group_10_values, group_11_values)
    started = request.method == "POST"
    return render_template(
        "grupo_10.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        group_8_values=group_8_values,
        group_9_values=group_9_values,
        group_11_values=group_11_values,
        fields=GROUP_10_FIELDS,
        values=group_10_values,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-11", methods=["GET", "POST"])
def grupo_11():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    group_8_values = build_group_8_values(source_data)
    group_9_values = build_group_9_values(source_data)
    group_10_values = build_group_10_values(source_data)
    group_11_values = build_group_11_values(source_data)
    group_12_values = build_group_12_values(source_data)
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(
        group_1_values,
        group_2_values,
        group_3_values,
        group_4_values,
        group_5_values,
        group_6_values,
        group_7_values,
        robot_name,
        group_8_values,
        group_9_values,
        group_10_values,
        group_11_values,
        group_12_values,
    )
    started = request.method == "POST"
    return render_template(
        "grupo_11.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        group_8_values=group_8_values,
        group_9_values=group_9_values,
        group_10_values=group_10_values,
        group_12_values=group_12_values,
        fields=GROUP_11_FIELDS,
        values=group_11_values,
        calc_mode=calc_mode,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-12", methods=["GET", "POST"])
def grupo_12():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    group_8_values = build_group_8_values(source_data)
    group_9_values = build_group_9_values(source_data)
    group_10_values = build_group_10_values(source_data)
    group_11_values = build_group_11_values(source_data)
    group_12_values = build_group_12_values(source_data)
    group_13_values = build_group_13_values(source_data)
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(
        group_1_values,
        group_2_values,
        group_3_values,
        group_4_values,
        group_5_values,
        group_6_values,
        group_7_values,
        robot_name,
        group_8_values,
        group_9_values,
        group_10_values,
        group_11_values,
        group_12_values,
        group_13_values,
    )
    started = request.method == "POST"
    return render_template(
        "grupo_12.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        group_8_values=group_8_values,
        group_9_values=group_9_values,
        group_10_values=group_10_values,
        group_11_values=group_11_values,
        group_13_values=group_13_values,
        fields=GROUP_12_FIELDS,
        values=group_12_values,
        calc_mode=calc_mode,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-13", methods=["GET", "POST"])
def grupo_13():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    group_8_values = build_group_8_values(source_data)
    group_9_values = build_group_9_values(source_data)
    group_10_values = build_group_10_values(source_data)
    group_11_values = build_group_11_values(source_data)
    group_12_values = build_group_12_values(source_data)
    group_13_values = build_group_13_values(source_data)
    group_14_values = build_group_14_values(source_data)
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(
        group_1_values,
        group_2_values,
        group_3_values,
        group_4_values,
        group_5_values,
        group_6_values,
        group_7_values,
        robot_name,
        group_8_values,
        group_9_values,
        group_10_values,
        group_11_values,
        group_12_values,
        group_13_values,
        group_14_values,
    )
    started = request.method == "POST"
    return render_template(
        "grupo_13.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        group_8_values=group_8_values,
        group_9_values=group_9_values,
        group_10_values=group_10_values,
        group_11_values=group_11_values,
        group_12_values=group_12_values,
        group_14_values=group_14_values,
        fields=GROUP_13_FIELDS,
        values=group_13_values,
        calc_mode=calc_mode,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-14", methods=["GET", "POST"])
def grupo_14():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    source_data = request.form if request.method == "POST" else request.args
    group_1_values = build_group_1_values(source_data)
    group_2_values = build_group_2_values(source_data)
    group_3_values = build_group_3_values(source_data)
    group_4_values = build_group_4_values(source_data)
    group_5_values = build_group_5_values(source_data)
    group_6_values = build_group_6_values(source_data)
    group_7_values = build_group_7_values(source_data)
    group_8_values = build_group_8_values(source_data)
    group_9_values = build_group_9_values(source_data)
    group_10_values = build_group_10_values(source_data)
    group_11_values = build_group_11_values(source_data)
    group_12_values = build_group_12_values(source_data)
    group_13_values = build_group_13_values(source_data)
    group_14_values = build_group_14_values(source_data)
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(
        group_1_values,
        group_2_values,
        group_3_values,
        group_4_values,
        group_5_values,
        group_6_values,
        group_7_values,
        robot_name,
        group_8_values,
        group_9_values,
        group_10_values,
        group_11_values,
        group_12_values,
        group_13_values,
        group_14_values,
    )
    started = request.method == "POST"
    return render_template(
        "grupo_14.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
        group_5_values=group_5_values,
        group_6_values=group_6_values,
        group_7_values=group_7_values,
        group_8_values=group_8_values,
        group_9_values=group_9_values,
        group_10_values=group_10_values,
        group_11_values=group_11_values,
        group_12_values=group_12_values,
        group_13_values=group_13_values,
        fields=GROUP_14_FIELDS,
        values=group_14_values,
        calc_mode=calc_mode,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-1/download", methods=["POST"])
def grupo_1_download():
    group_1_values = build_group_1_values(request.form)
    group_2_values = build_group_2_values(request.form)
    group_3_values = build_group_3_values(request.form)
    group_4_values = build_group_4_values(request.form)
    group_5_values = build_group_5_values(request.form)
    group_6_values = build_group_6_values(request.form)
    group_7_values = build_group_7_values(request.form)
    group_8_values = build_group_8_values(request.form)
    group_9_values = build_group_9_values(request.form)
    group_10_values = build_group_10_values(request.form)
    group_11_values = build_group_11_values(request.form)
    group_12_values = build_group_12_values(request.form)
    group_13_values = build_group_13_values(request.form)
    group_14_values = build_group_14_values(request.form)
    robot_name = sanitize_robot_name(request.form.get("robot"))
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, group_5_values, group_6_values, group_7_values, robot_name, group_8_values, group_9_values, group_10_values, group_11_values, group_12_values, group_13_values, group_14_values)
    return Response(
        set_content,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{robot_name}_grupo_1_inicial.set"'},
    )


if __name__ == "__main__":
    app.run(debug=True)
