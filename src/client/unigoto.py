import time
from typing import Literal
from datetime import datetime
from functools import partial
from collections.abc import Iterable

import pandas as pd
import requests
import streamlit as st

from config import *

st.text_input = partial(st.text_input, label_visibility="collapsed")


def _get_results_name() -> str:
    return f"search_results_{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}"


def _write_as_list(input_data: Iterable) -> None:
    for item in input_data:
        st.markdown(f"* {item}")


def _call_api(
    url: str,
    request: dict = None,
    call_type: Literal["get", "post"] = "get",
) -> dict:
    if call_type == "get":
        response = requests.get(url)
    elif call_type == "post":
        response = requests.post(
            url,
            json=request,
            timeout=180,
        )
    else:
        raise ValueError(f"`call_type` should be 'get' or 'post', not `{call_type}`")
    if response.status_code != 200:
        st.error(f"error {response.status_code} {response.content}")
    return response.json()


def _parse_response(
    response: dict,
    show_id: bool = False,
    show_metrics: bool = False,
) -> pd.DataFrame:
    df = pd.DataFrame(response["items"])
    df.index = df.index + 1
    if not show_id:
        df.drop(columns=[col for col in df.columns if "_id" in col], inplace=True)
    if not show_metrics:
        df.drop(columns=METRICS, inplace=True)
    return df


def main():
    # Sidebar
    with st.sidebar:
        st.markdown(
            "# Big Ear + UniGoTo 👨‍🎓👩‍🎓\nС помощью нашего приложения ты сможешь подобрать себе лучший университет!\n"
        )
        with st.expander("Продвинутые настройки"):
            limit = st.slider(
                "Лимит выдачи результатов",
                min_value=1,
                max_value=50,
                value=20,
                step=1,
            )
            show_id = st.checkbox("Показывать id")
            show_metrics = st.checkbox("Показывать метрики")
        with st.expander("Проверить работу API"):
            if st.button("Ping"):
                response = _call_api(ENDPOINT_PING)
                success = st.success(response["response"])
                time.sleep(1)
                success.empty()
        st.markdown("## Информация")
        with st.expander("Участники"):
            _write_as_list(CONTRIBUTORS_MD)
        with st.expander("Ссылки"):
            _write_as_list(LINKS_MD)
        with st.expander("Версии"):
            _write_as_list(VERSIONS_MD)

    # User input
    st.markdown("## Расскажи нам про себя")
    with st.expander("Здесь находятся поля для заполнения", expanded=True):
        auto_fill = st.checkbox("Заполнить автоматически  / очистить поля")
        request = REQUEST_BODY.copy()
        for index, item in enumerate(USER_INPUT):
            st.markdown(f"##### {item['markdown']}")
            args = (f"{index}", item["example"]) if auto_fill else f"{index}"
            request[item["option"]] = st.text_input(*args)
    request["limit"] = limit

    # Analysis and results
    if st.button("Отправить на анализ", use_container_width=True):
        with st.spinner("Обработка..."):
            response = _call_api(ENDPOINT_SEARCH, request, "post")
        if response["items"]:
            st.success("Done!")
            st.markdown("## Результаты анализа")
            result_table = _parse_response(response, show_id, show_metrics)
            st.download_button(
                label="Скачать таблицу",
                data=result_table.to_csv().encode("utf-8"),
                file_name=f"{_get_results_name()}.csv",
                mime="text/csv",
                help="В формате csv",
            )
            st.table(result_table)
        else:
            st.error("Результаты не найдены. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    st.set_page_config(page_title="Подбор университета")
    main()
