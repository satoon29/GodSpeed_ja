"""
記載している日本語は全て以下の論文から引用
Godspeed Questionnaire Series: Translations and Usage, 2023
https://www.bartneck.de/publications/2023/godspeed/bartneckGodspeedChapter2023.pdf
"""
import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import gspread
from google.oauth2.service_account import Credentials


KEY = 0

def insert_scale(q):
    with q[1]:
        five_lickert1 = st.columns(5)
        with five_lickert1[0]:
            st.markdown("**1**")
        with five_lickert1[1]:
            st.markdown("**2**")
        with five_lickert1[2]:
            st.markdown("**3**")
        with five_lickert1[3]:
            st.markdown("**4**")
        with five_lickert1[4]:
            st.markdown("**5**")
    return


def set_question(q, left, right):

    global KEY

    with q[0]:
        st.markdown(left)

    with q[1]:
        lickert = st.columns(5)
        with lickert[0]:
            s1 = st.checkbox(label="1", key=KEY, label_visibility="hidden")
            KEY += 1
        with lickert[1]:
            s2 = st.checkbox(label="2", key=KEY, label_visibility="hidden")
            KEY += 1
        with lickert[2]:
            s3 = st.checkbox(label="3", key=KEY, label_visibility="hidden")
            KEY += 1
        with lickert[3]:
            s4 = st.checkbox(label="4", key=KEY, label_visibility="hidden")
            KEY += 1
        with lickert[4]:
            s5 = st.checkbox(label="5", key=KEY, label_visibility="hidden")
            KEY += 1

        checked = any([s1, s2, s3, s4, s5])
        if checked:
            score = int([s1, s2, s3, s4, s5].index(True)) + 1
        else:
            score = 0

    with q[2]:
        st.markdown(right)

    return score, f"{left}_{right}"


if __name__ == "__main__":

    date = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    file_name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    st.title("ロボットの印象評価アンケート")
    st.markdown(f"```実施日: {date}```")
    st.markdown("以下のスケールに基づいて、このロボットに対するあなたの印象を評価してください。\
                左側の言葉があなたの印象に近い場合は1に、右側の言葉があなたの印象に近い場合は5に、その中間である場合は2、3、4に印を付けてください。")

    log = list()
    log.append(["カテゴリ", "質問", "評価値"])

    # 擬人観
    st.divider()
    insert_scale(st.columns(3))
    g1, q1 = set_question(st.columns(3), "偽物のような", "自然な")
    g2, q2 = set_question(st.columns(3), "機械的", "人間的")
    g3, q3 = set_question(st.columns(3), "意識を持たない", "意識を持っている")
    g4, q4 = set_question(st.columns(3), "人工的", "生物的")
    g5, q5 = set_question(st.columns(3), "ぎこちない動き", "洗練された動き")
    g = [g1, g2, g3, g4, g5]
    ave_g = sum(g) / len(g)

    log.append(["擬人観", q1, g1])
    log.append(["擬人観", q2, g2])
    log.append(["擬人観", q3, g3])
    log.append(["擬人観", q4, g4])
    log.append(["擬人観", q5, g5])

    # 有生性
    st.divider()
    insert_scale(st.columns(3))
    y1, q1 = set_question(st.columns(3), "死んでいる", "生きている")
    y2, q2  = set_question(st.columns(3), "活気のない", "生き生きとした")
    y3, q3  = set_question(st.columns(3), "機械的な", "有機的な")
    y4, q4  = set_question(st.columns(3), "人工的な", "生物的な")
    y5, q5  = set_question(st.columns(3), "不活発な", "対話的な")
    y6, q6  = set_question(st.columns(3), "無関心な", "反応のある")
    y = [y1, y2, y3, y4, y5, y6]
    ave_y = sum(y) / len(y)

    log.append(["有生性", q1, y1])
    log.append(["有生性", q2, y2])
    log.append(["有生性", q3, y3])
    log.append(["有生性", q4, y4])
    log.append(["有生性", q5, y5])
    log.append(["有生性", q6, y6])

    # 好感度
    st.divider()
    insert_scale(st.columns(3))
    k1, q1 = set_question(st.columns(3), "嫌い", "好き")
    k2, q2 = set_question(st.columns(3), "親しみにくい", "親しみやすい")
    k3, q3 = set_question(st.columns(3), "不親切な", "親切な")
    k4, q4 = set_question(st.columns(3), "不愉快な", "愉快な")
    k5, q5 = set_question(st.columns(3), "ひどい", "良い")
    k = [k1, k2, k3, k4, k5]
    ave_k = sum(k) / len(k)

    log.append(["好感度", q1, k1])
    log.append(["好感度", q2, k2])
    log.append(["好感度", q3, k3])
    log.append(["好感度", q4, k4])
    log.append(["好感度", q5, k5])

    # 知性の有無
    st.divider()
    insert_scale(st.columns(3))
    t1, q1 = set_question(st.columns(3), "無能な", "有能な")
    t2, q2  = set_question(st.columns(3), "無知な", "物知りな")
    t3, q3  = set_question(st.columns(3), "無責任な", "責任のある")
    t4, q4  = set_question(st.columns(3), "知的でない", "知的な")
    t5, q5  = set_question(st.columns(3), "愚かな", "賢明な")
    t = [t1, t2, t3, t4, t5]
    ave_t = sum(t) / len(t)

    log.append(["知性の有無", q1, t1])
    log.append(["知性の有無", q2, t2])
    log.append(["知性の有無", q3, t3])
    log.append(["知性の有無", q4, t4])
    log.append(["知性の有無", q5, t5])

    # 安心感の有無
    st.divider()
    insert_scale(st.columns(3))
    a1, q1 = set_question(st.columns(3), "不安な", "落ち着いた")
    a2, q2 = set_question(st.columns(3), "冷静な", "動揺している")
    a3, q3 = set_question(st.columns(3), "平穏な", "驚いた")
    a = [a1, a2, a3]
    ave_a = sum(a) / len(a)

    log.append(["安心感の有無", q1, a1])
    log.append(["安心感の有無", q2, a2])
    log.append(["安心感の有無", q3, a3])


    df = pd.DataFrame(
        dict(r=[ave_g, ave_y, ave_k, ave_t, ave_a],
            theta=[
                "擬人観",
                "有生性",
                "好感度",
                "知性の有無",
                "安心感の有無"
                ]
            )
    )

    if st.button("完了"):

        # ローカルCSVファイルに保存
        with open(f"{file_name}.csv", mode="w", encoding="utf-8") as o:
            o.write("カテゴリ,質問,評価値\n")
            for row in log[1:]:
                o.write(f"{row[0]},{row[1]},{row[2]}\n")

        # Google Spread Sheetに保存
        try:
            # 認証情報の設定（Streamlit Secretsから取得）
            credentials = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=[
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
            )
            
            client = gspread.authorize(credentials)
            
            # スプレッドシートを開く（URLまたはキーで指定）
            spreadsheet = client.open_by_key(st.secrets["spreadsheet_key"])
            worksheet = spreadsheet.sheet1
            
            # タイムスタンプを追加して書き込み
            for row in log[1:]:
                worksheet.append_row([date] + row)
            
            st.success("データをGoogle Spread Sheetに保存しました！")
            
        except Exception as e:
            st.error(f"Google Spread Sheetへの保存に失敗しました: {e}")

        # グラフの生成と保存
        fig = go.Figure()
        fig.add_trace(
            go.Scatterpolar(
                r=df["r"],
                theta=df["theta"],
                fill='toself',
                name='モデル名',
                # line_color="#EF553B",
                fillcolor="#9467BD",
                opacity=0.3
                )
            )
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                    )
                ),
                showlegend=True
            )
        fig.show()
        fig.write_image(f"{file_name}.png", scale=2)
