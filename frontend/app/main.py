import requests
import streamlit as st
import matplotlib.pyplot as plt


st.title('Расчет справедливой цены опциона')
models = ["Модель Хестона", "Модель Блэка-Шоулса", "Модель Блэка-Шоулса (модифицированная)"]
model = st.selectbox("Выберите модель",models)


if model == "Модель Хестона":
    st.header("Модель Хестона")

    st.text("Модель Хестона – это математическая модель, предложенная Стивеном Хестоном, \n"
            "где цена актива определяется стохастическим процессом:")
    st.latex("d{S_t}=rS_tdt+S_t\sqrt{V_t}d\mathrm{W}_{t}^{S}")

    st.text("а волатильность цены задается процессом:")
    st.latex("dV_t=k(\\theta-V_t) + \sigma\sqrt{V_t}d\mathrm{W}_{t}^{V}")
    st.write("$S_t$ – цена актива в момент времени t")
    st.write("$r$ – безрисковая процентная ставка")
    st.write("$\sqrt{V_t}$ – волатильность цены актива")
    st.write("$\sigma$ – волатильность волатильности $\sqrt{V_t}$")
    st.write("$\\theta$ – долгосрочная дисперсия цены")
    st.write("$k$ – скорость возврата к долгосрочной дисперсии цены")
    st.write("$dt$ – неопределенно малый положительный временной прирост")
    st.write("$W_t^S$ – броуновское движение цены актива")
    st.write("$W_t^V$ – броуновское движение дисперсии цены актива")
    st.write("$\\rho$ – коэффициент корреляции для $W_t^S$ и $W_t^V$")


    st.subheader("Введите необходимые параметры")

    K = st.text_input("Цена страйк: ")
    T = st.text_input("Время исполнения контракта: ")
    V0 = st.text_input("Волатильность актива в начальный момент времени: ")
    k = st.text_input("Скорость возвращения к долгосрочной дисперсии цены: ")
    theta = st.text_input("Долгосрочная дисперсия цены: ")
    r = st.text_input("Безрисковая процентная ставка: ")
    S0 = st.text_input("Цена актива в начальный момент времени: ")
    ro = st.text_input("Коэффициент корреляции между $W_t^S$ и $W_t^V$: ")
    input_json = dict(
        V0=V0,
        T=T,
        k=k,
        theta=theta,
        r=r,
        S0=S0,
        K=K,
        ro=ro,
    )

    if st.button("Рассчитать справедливую цену"):
        st.subheader("Справедливая цена расчитанная методом Монте-Карло с аппроксимацией нормальными случайными величинами:")
        res_norm = requests.post(f"http://backend:8000/heston_norm", json=input_json)
        st.text(res_norm.json())

        st.subheader("Справедливая цена расчитанная методом Монте-Карло с аппроксимацией бинарными случайными величинами:")
        res_bin = requests.post(f"http://backend:8000/heston_bin", json=input_json)
        st.text(res_bin.json())

        st.subheader("Интервал справедливых цен:")
        res_interval = requests.post(f"http://backend:8000/heston_interval", json=input_json)
        st.text(res_interval.json()[1])
        st.subheader("График значений цены опциона в 100 опытах:")
        fig, ax = plt.subplots()
        ax.plot(res_interval.json()[0])
        st.pyplot(fig)



elif model == "Модель Блэка-Шоулса":
    S0 = st.text_input("S0: ")
    K = st.text_input("K: ")
    r = st.text_input("r: ")
    sigma = st.text_input("sigma: ")
    T = st.text_input("T: ")

    input_json = dict(
        S0=S0,
        K=K,
        r=r,
        sigma=sigma,
        T=T,
    )

    if st.button("price"):
        st.subheader("Справедливая цена расчитанная с помощью формулы Блэка-Шоулса:")
        res_norm = requests.post(f"http://backend:8000/black_scholes", json=input_json)
        st.text(res_norm.json())

        st.subheader("Справедливая цена расчитанная методом Монте-Карло с аппроксимацией \n"
                "нормальными случайными величинами:")
        res_bin = requests.post(f"http://backend:8000/black_scholes_monte_carlo", json=input_json)
        st.text(res_bin.json())

        st.subheader("Справедливая цена расчитанная методом Монте-Карло с помощью \n"
                "рекуррентных формул:")
        res_bin = requests.post(f"http://backend:8000/black_scholes_binomial", json=input_json)
        st.text(res_bin.json())