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


def sanitize_calc_mode(raw_value):
    return raw_value if raw_value in ("pts", "pct") else "pts"


def build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, setup_name: str):
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
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, robot_name)
    return render_template("index.html", robot_name=robot_name, values=group_1_values, group_2_values=group_2_values, group_3_values=group_3_values, group_4_values=group_4_values, set_content=set_content)


@app.route("/iniciar", methods=["POST"])
def iniciar():
    robot_name = sanitize_robot_name(request.form.get("robot_name"))
    group_1_values = build_group_1_values(request.form)
    group_2_values = build_group_2_values(request.form)
    group_3_values = build_group_3_values(request.form)
    group_4_values = build_group_4_values(request.form)
    return redirect(
        url_for(
            "grupo_1",
            robot=robot_name,
            m_magic=group_1_values["m_magic"],
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
    flow_values = build_group_1_flow_values(source_data)
    set_content = build_set_content(values, group_2_values, group_3_values, group_4_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_1.html",
        fields=GROUP_1_FIELDS,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
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
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_2.html",
        group_1_values=group_1_values,
        fields=GROUP_2_FIELDS,
        values=group_2_values,
        group_3_values=group_3_values,
        group_4_values=group_4_values,
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
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_3.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        fields=GROUP_3_FIELDS,
        values=group_3_values,
        group_4_values=group_4_values,
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
    calc_mode = sanitize_calc_mode(request.values.get("calc_mode"))
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, robot_name)
    started = request.method == "POST"
    return render_template(
        "grupo_4.html",
        group_1_values=group_1_values,
        group_2_values=group_2_values,
        group_3_values=group_3_values,
        fields=GROUP_4_FIELDS,
        values=group_4_values,
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
    robot_name = sanitize_robot_name(request.form.get("robot"))
    set_content = build_set_content(group_1_values, group_2_values, group_3_values, group_4_values, robot_name)
    return Response(
        set_content,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{robot_name}_grupo_1_inicial.set"'},
    )


if __name__ == "__main__":
    app.run(debug=True)
