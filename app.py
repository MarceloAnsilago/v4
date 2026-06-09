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


def build_group_1_set_content(values):
    return "\n".join(
        [
            "; Grupo 1 - Parametrizacao Inicial",
            f"m_magic={values['m_magic']}",
            f"m_processo={values['m_processo']}",
            f"m_mercado={values['m_mercado']}",
            f"m_validade={values['m_validade']}",
        ]
    )


app = Flask(__name__)


@app.route("/")
def index():
    robot_name = sanitize_robot_name(request.args.get("robot"))
    return render_template("index.html", robot_name=robot_name)


@app.route("/iniciar", methods=["POST"])
def iniciar():
    robot_name = sanitize_robot_name(request.form.get("robot_name"))
    return redirect(url_for("grupo_1", robot=robot_name))


@app.route("/grupo-1", methods=["GET", "POST"])
def grupo_1():
    robot_name = sanitize_robot_name(request.values.get("robot"))
    values = build_group_1_values(request.form if request.method == "POST" else None)
    set_content = build_group_1_set_content(values)
    started = request.method == "POST"
    return render_template(
        "grupo_1.html",
        fields=GROUP_1_FIELDS,
        values=values,
        set_content=set_content,
        started=started,
        robot_name=robot_name,
    )


@app.route("/grupo-1/download", methods=["POST"])
def grupo_1_download():
    values = build_group_1_values(request.form)
    set_content = build_group_1_set_content(values)
    robot_name = sanitize_robot_name(request.form.get("robot"))
    return Response(
        set_content,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{robot_name}_grupo_1_inicial.set"'},
    )


if __name__ == "__main__":
    app.run(debug=True)
