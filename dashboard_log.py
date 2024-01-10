import streamlit as st
import pydeck as pdk
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta
#from st_tabs import TabBar


st.set_page_config(layout="wide")

for i in range(3):
    st.columns(1)

#component1=  TabBar(tabs=['메인화면','CCTV','CCTV화면'],default=0,background = "#000000",color="#FFFFFF",activeColor="blue",fontSize="15px")
tab1,tab2,tab3 = tabs['메인화면','CCTV','CCTV화면']
with tab1:
#if (component1 == 0):
#     st.markdown("""
#     <style>
    
#         .stTabs [data-baseweb="tab-list"] {
#             gap: 5px;
#         }
    
#         .stTabs [data-baseweb="tab"] {
#             height: 50px;
#             margin : 0px;
#             font-color : #FFFFFF;
#             background-color: #F0F2F6;
#         }
    
#         .stTabs [aria-selected="true"] {
#             background-color: #000000;
#         }

#     </style>""", unsafe_allow_html=True)


    def load_cctv_content():

        st.markdown(
            """
            <style>
            .stApp {
                background-color: #333333;
            }
            /* Remove padding and margin from the main block */
            .block-container {
                    padding-top: 1rem; /* 위에 패딩 */
                    padding-right: 1rem; /* 오른쪽 패딩 */
                    padding-left: 1rem; /* 왼쪽 패딩 */
                    padding-bottom: 1rem; /* 아래 패딩 */
                }

                /* 스트림릿의 칼럼 사이 간격 조정 */
                .st-cx {
                    margin: 0; /* 외부 여백 제거 */
                }

                /* 칼럼 내부의 패딩 조정 */
                .st-cc {
                    padding:0.5rem; /* 좌우 패딩 */
                }
                .st-de { 
                    margin-left: 0px; 
                    margin-right: 0px; 
                }
                /* 칼럼 내부의 패딩 조정 */
                .st-cy {
                    padding: 8px; /* 상하좌우 패딩을 8px로 설정 */
                }
            </style>
            </style>
            """,
            unsafe_allow_html=True
        )



        # 상단바 스타일과 컴포넌트 정의
        st.markdown("""

        <style>

        .header {
            background-color:black;
            color: white;
            padding: 10px 0px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .logo {
            flex-grow: 2;
            display: flex;
            align-items: center;
        }
        .logo > img {
            margin-right: 20px;
        }

        .logo-text {
            display: flex;
            align-items: center;
            font-size: 24px; /* 텍스트 크기 증가 */
            font-weight: bold;
            margin-right: 20px; /* 오른쪽 여백 추가 */
            color : #eeeeee;
        }

        .search-box {
            display: flex;
            justify-content: right;
        }

        .search-input {
            background-color: #999999; /* 검색창 배경색 */
            color: white; /* 검색창 텍스트 색상 */
            margin: 0px 10px;
            padding: 10px 15px; /* 검색창 내부 패딩 */
            border-radius: 20px; /* 검색창 라운드 값 */
            border: 1px solid #004165; /* 검색창 테두리 색상 */
            outline: none; /* 클릭 시 발생하는 아웃라인 제거 */
        }
        .search-input::placeholder {
            color: white; /* 플레이스홀더 텍스트 색상을 흰색으로 설정 */
            opacity: 1; /* 플레이스홀더 텍스트의 불투명도를 100%로 설정 */
        }
        .notifications {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            margin-left: 20px; /* 왼쪽 여백 추가 */
            font-size: 12px;
        }
        .clock {
            display: flex;
            align-items: center;
            margin-left: 20px; /* 왼쪽 여백 추가 */
            font-size: 18px;
        }
        </style>
        """, unsafe_allow_html=True)

        # 상단바 컴포넌트
        st.markdown("""
        <div class="header">
            <div class="logo">
                <img src="http://localhost:8888/files/bigproject_dashboard/%EB%A1%9C%EA%B3%A0.png?_xsrf=2%7Cccdf4ca1%7Cfa4c9db36c6598195a1c805cc167066d%7C1703818891" height="40"/>
                <div class="logo-text">CCTV</div>
            </div>
            <div class="search-box">
                <input class="search-input" type="text" placeholder="🔍 차량 번호 입력" />
                <input class="search-input" type="text" placeholder="🔍 노선, 정류장 입력" />
            </div>
            <div class="notifications">
                🔔 이벤트 12건
            </div>
            <div class="clock" id="clock">
                <!-- 시간 표시 -->
            </div>
        </div>
        """, unsafe_allow_html=True)




#---------------------------------------------------------------------------------------------
  



    # 상단바에 날짜와 시간을 표시하는 함수
    def display_time():
        time_display = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.markdown(f"<span style='color: white;'>🕒 {time_display}</span>", unsafe_allow_html=True)

    # 상태를 초기화하는 함수
    def initialize_state():
        st.session_state.remaining_seconds = 15 * 60  # 15분
        st.session_state.current_tab = '메인'
        st.session_state.current_speed = np.random.randint(275, 285)
        st.session_state.alert_active = False
        st.session_state.alert = False  # 'alert' 키 초기화
        st.session_state.workers_data_updated = False
        st.session_state.auto_update = False
        st.session_state.workers_data = create_initial_data()


    # 작업자 데이터 생성 함수
    def create_initial_data():
        last_names = ["김", "고", "박", "최", "정", "강", "조", "윤", "장", "임"]
        first_names = ["영수", "영호", "영식", "영철", "성호", "성수", "지만", "병철", "철수", "한철"]
        base_latitude, base_longitude = 37.611294, 126.830462
        num_workers = 20

        np.random.seed(42)
        data = pd.DataFrame({
            'latitude': np.random.normal(loc=base_latitude, scale=0.0005, size=num_workers),
            'longitude': np.random.normal(loc=base_longitude, scale=0.0005, size=num_workers),
            'status': ['정상' for _ in range(num_workers)],
            'worker_id': [np.random.choice(last_names) + np.random.choice(first_names) for _ in range(num_workers)],
            'task': np.random.choice(['전기 설비', '신호 검사', '선로 점검'], size=num_workers),
            'start_time': '09:00',
            'end_time': '18:00',
        })

        return data

    def update_data(data):
        if 'update_time' not in st.session_state:
            st.session_state.update_time = time.time() + 10

        current_time = time.time()
        if current_time > st.session_state.update_time:
            if data.at[0, 'status'] == '정상':
                data.at[0, 'status'] = '이상상황발생'
                # 경고를 10초 뒤에 활성화
                st.session_state.alert_time = time.time() + 10
                st.session_state.alert = True  # 경고 상태 활성화
                st.session_state.update_time += 10  # 추가 업데이트를 위해 시간을 늘림

        # 각 행의 상태에 따라 색상 지정 (투명도 수정)
        data['color'] = data['status'].apply(lambda x: [0, 0, 255] if x == '정상' else [255, 255, 0, 255])
        return data


    # 작업자 데이터 업데이트 함수
    def update_worker_data():
        # 작업자 위치 업데이트 로직
        for index, worker in st.session_state.workers_data.iterrows():
            st.session_state.workers_data.at[index, 'latitude'] += np.random.uniform(-0.0001, 0.0001)
            st.session_state.workers_data.at[index, 'longitude'] += np.random.uniform(-0.0001, 0.0001)

        # 경고 상태 관리 로직
        current_time = time.time()
        if st.session_state.auto_update and 'alert_time' in st.session_state:
            if current_time > st.session_state.alert_time and not st.session_state.alert_active:
                st.session_state.alert_active = True
                # 첫 번째 작업자의 상태를 'issue'로 변경
                st.session_state.workers_data.at[0, 'status'] = '이상상황 발생'
                st.session_state.workers_data.at[0, 'color'] = [255, 255, 0, 160]  # 노란색

    def display_fullscreen_alert():
        update_alert_state()
        alert_container = st.empty()  # 경고창을 위한 컨테이너 생성

        if st.session_state['alert']:
            with alert_container:
                st.markdown(
                    """
                    <style>
                    .overlay {
                        position: fixed;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background-color: rgba(0,0,0,0.5);
                        z-index: 999;
                        animation: blinker 3s linear 3;
                    }
                    @keyframes blinker {
                        50% { opacity: 0; }
                    }
                    .alert-box {
                        background-color: #ffcc00;
                        color: black;
                        padding: 20px;
                        border-radius: 5px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 500px;
                    }
                    </style>
                    <div class="overlay">
                        <div class="alert-box">
                            <strong>경고:</strong> 주의가 필요한 상황이 감지되었습니다.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            time.sleep(7)  # 7초간 대기
            alert_container.empty()  # 경고창 컨테이너 비우기
            st.session_state.alert = False  # 경고 상태를 False로 설정


    def update_alert_state():
        if 'alert_time' in st.session_state:
            elapsed_time = time.time() - st.session_state.alert_time
            if elapsed_time > 10:
                st.session_state.alert = False
                del st.session_state.alert_time


    # 업무 시작 버튼 처리 함수

    def start_work():
        initialize_state()
        st.session_state.auto_update = True
        st.session_state.alert_time = time.time() + 10  # 10초 후에 경고 활성화

    # 경고창 및 Tooltip 표시 함수
    def display_alert_and_tooltip():
        if st.session_state.alert_active:
            st.markdown("경고: 주의가 필요한 상황이 감지되었습니다.", unsafe_allow_html=True)
            time.sleep(3)
            st.empty()  # 경고창 숨김
            display_tooltip(st.session_state.workers_data, 0)  # 첫 번째 작업자의 Tooltip 표시
        elif st.session_state.alert:
            st.markdown("<div style='color: red;'>경고: 주의가 필요한 상황이 감지되었습니다.</div>", unsafe_allow_html=True)
            time.sleep(1)
            st.empty()
            display_tooltip(st.session_state.workers_data, 0)  # 첫 번째 작업자의 Tooltip 표시

    # Tooltip 표시 함수
    def display_tooltip(data, index):
        worker = data.iloc[index]
        tooltip_html = f"""
        <div style='background-color: white; padding: 10px; border-radius: 5px;'>
            <strong>작업자명:</strong> {worker['worker_id']}<br>
            <strong>작업:</strong> {worker['task']}<br>
            <strong>근무 시간:</strong> {worker['start_time']} - {worker['end_time']}<br>
            <strong>현재 상태:</strong> {worker['status']}
        </div>
        """
        st.markdown(tooltip_html, unsafe_allow_html=True)

    # 상태 업데이트 함수
    def update_state():
        if st.session_state.auto_update:
            st.session_state.remaining_seconds -= 1
            if st.session_state.remaining_seconds <= 0:
                st.session_state.remaining_seconds = 15 * 60  # 타이머 리셋
            st.session_state.current_speed = np.random.randint(275, 285)  # 속도 랜덤 업데이트
            update_worker_data()
            display_alert_and_tooltip()


    if 'vehicle_time' not in st.session_state:
        st.session_state.vehicle_time = 60  # 예: 60초로 시작
    def on_main_tab_clicked():
        st.session_state.vehicle_time -= 10  # 예: 10초 감소
        st.write(f"차량 접근 시간: {st.session_state.vehicle_time}초")

    # -----------------------------------------------------------------------------------------------------
    # 스타일을 위한 CSS 추가
    def add_custom_css():
        st.markdown("""
        <style>
        .tab-button {
            background-color: black;
            color: white;
            padding: 10px;
            border: none;
            margin: 0px; /* Remove space between buttons */
            cursor: pointer;
            width: 100%; /* Set the width of buttons to be equal */
        }
        .tab-button:hover {
            background-color: #555;
        }
        /* Remove gap between columns */
        .column {
            padding: 0px !important;
        }
        </style>
        """, unsafe_allow_html=True)

    add_custom_css()
    # 초기 상태 설정
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = '메인'

    # 초기 상태 설정
    if 'initialized' not in st.session_state:
        initialize_state()
        st.session_state.initialized = True

    # 탭 선택 부분
    if st.session_state.current_tab == 'CCTV':
        with right_column:
            load_cctv_content()

    if st.session_state.current_tab == '메인':
        on_main_tab_clicked()


    # UI 구성
    # display_time()

    st.markdown(
            """
            <style>
            .stApp {
                background-color: #333333;
            }
            /* Remove padding and margin from the main block */
            .block-container {
                    padding-top: 1rem; /* 위에 패딩 */
                    padding-right: 1rem; /* 오른쪽 패딩 */
                    padding-left: 1rem; /* 왼쪽 패딩 */
                    padding-bottom: 1rem; /* 아래 패딩 */
                }


            </style>
            """,
            unsafe_allow_html=True
        )

        # 상단바 스타일과 컴포넌트 정의
    st.markdown("""

        <style>

        .header {
            background-color:black;
            color: white;
            padding: 10px 0px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .logo {
            flex-grow: 2;
            display: flex;
            align-items: center;
        }
        .logo > img {
            margin-right: 20px;
        }

        .logo-text {
            display: flex;
            align-items: center;
            font-size: 18px; /* 텍스트 크기 증가 */
            font-weight: bold;
            margin-right: 20px; /* 오른쪽 여백 추가 */
            color : #eeeeee;
        }

        .search-box {
            display: flex;
            justify-content: right;
        }

        .search-input {
            background-color: #999999; /* 검색창 배경색 */
            color: white; /* 검색창 텍스트 색상 */
            margin: 0px 15px;
            padding: 5px 10px; /* 검색창 내부 패딩 */
            border-radius: 15px; /* 검색창 라운드 값 */
            border: 1px solid #004165; /* 검색창 테두리 색상 */
            outline: none; /* 클릭 시 발생하는 아웃라인 제거 */
        }
        .search-input::placeholder {
            color: white; /* 플레이스홀더 텍스트 색상을 흰색으로 설정 */
            opacity: 1;
            font-size: 13.5px;/* 플레이스홀더 텍스트의 불투명도를 100%로 설정 */
        }
        .notifications {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            margin-left: 20px; /* 왼쪽 여백 추가 */
            font-size: 13px;
        }
        .clock {
            display: flex;
            align-items: center;
            margin-left: 20px; /* 왼쪽 여백 추가 */
            font-size: 18px;
        }
        </style>
        """, unsafe_allow_html=True)

        # 상단바 컴포넌트
    st.markdown("""
        <div class="header">
            <div class="logo">
                <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EB%A1%9C%EA%B3%A0.png?_xsrf=2%7C0e3e6c52%7C422d2d71a416b56c278b7c7591d926ef%7C1704801015" height="40"/>
                <div class="logo-text">수도권 철도 차량기지 관제센터</div>
            </div>
            <div class="search-box">
                <input class="search-input" type="text" placeholder="🔍 차량 번호 입력" />
                <input class="search-input" type="text" placeholder="🔍 역 이름 입력" />
            </div>
            <div class="notifications">
                🔔 이벤트 12건
            </div>
            <div class="clock" id="clock">
                <!-- 시간 표시 -->
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 실시간 시간 업데이트 스크립트
    st.markdown("""
        <script>
        function updateClock() {
            var now = new Date(),
                year = now.getFullYear(),
                month = now.getMonth() + 1,
                day = now.getDate(),
                hour = now.getHours(),
                minute = now.getMinutes(),
                second = now.getSeconds();
            if(month < 10) month = '0' + month;
            if(day < 10) day = '0' + day;
            if(hour < 10) hour = '0' + hour;
            if(minute < 10) minute = '0' + minute;
            if(second < 10) second = '0' + second;
            document.getElementById('clock').innerHTML = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
            setTimeout(updateClock, 1000);
        }
        updateClock(); // 초기 호출
        </script>
        """, unsafe_allow_html=True)


    # 화면 분할 설정 - 왼쪽에 탭, 오른쪽에 파일 내용
    left_column, right_column = st.columns([1, 18])

    # 왼쪽 컬럼에 탭 버튼 배치
    with left_column:
        tab_buttons = {
            '메인': '메인',
            'CCTV': 'CCTV',
            '분석': '분석'
        }
        for tab_key, tab_value in tab_buttons.items():
            button_html = f"<button class='tab-button' onclick='window.location.href=\"?current_tab={tab_key}\"'>{tab_value}</button>"
            st.markdown(button_html, unsafe_allow_html=True)




    # 오른쪽 컬럼에 파일 내용 표시
    with right_column:
    # 넓은 레이아웃 설정




        # --------------------------------------------------------------------------------------------------

        with st.container():
            # 왼쪽 섹션 컴포넌트
            left_col, main_col, right_col = st.columns([2.3,5.4,2.3])

            with left_col:
                with st.container():


                    # 기상 상태 섹션 스타일 정의
                    st.markdown("""
                   <style>
                .weather-section {
                    background-color: #555555; /* 탁한 하늘색 */
                    padding: 15px; /* 안쪽 여백 */
                    margin-bottom: 3px; /* 아래쪽 여백 */
                    display: block; /* 블록 레벨 요소 */
                }
                .weather-title {
                    font-weight: bold; /* 굵은 글씨 */
                    color : #ffffff;
                    font-size: 17px; /* 제목 크기 */
                    margin-bottom: 8px; /* 제목 아래 여백 */
                    display: block; /* 블록 레벨 요소 */
                }
                .weather-content {
                    display: flex; /* 가로 정렬 */
                }
                .weather-icon {
                    font-size: 3em; /* 이모티콘 크기 */
                    margin-right: 10px; /* 아이콘 오른쪽 여백 */
                }
                .weather-info {
                    display: flex; /* 가로 정렬 */
                    flex-grow: 1; /* 남은 공간을 채움 */
                    color : #ffffff
                }
                .weather-col {
                    flex-grow: 1; /* 각 열이 가능한 모든 공간을 차지하도록 설정 */
                    margin-right: 10px; /* 열 오른쪽 여백 */
                    font-size: 13px;
                }
                .last-col {
                    margin-right: 0; /* 마지막 열은 오른쪽 여백 없음 */
                }
                </style>

                <div class="weather-section">
                    <div class="weather-title">현재 기상상태</div>
                    <div class="weather-content">
                        <div class="weather-icon">☀️</div>
                        <div class="weather-info">
                            <div class="weather-col">
                                온도: 2°C<br>
                                바람: 4m/s<br>
                                강수량: 0mm
                            </div>
                            <div class="weather-col last-col">
                                가시거리: 10km<br>
                                기압: 1010hPa<br>
                                미세먼지: 15㎍/m³
                            </div>
                        </div>
                    </div>
                </div>
                    """, unsafe_allow_html=True)


            # ----------------------------------------------------------------------------------------------------------------


                    # 메트릭 표시를 위한 스타일 정의
                    st.markdown("""
                    <style>
                    .train-section {
                        background-color: #555555; /* 연한 회색 */
                        padding: 10px; /* 안쪽 여백 */
                        margin-bottom: 3px; /* 아래쪽 여백 */
                        display: block; /* 블록 레벨 요소 */
                    }
                    .train-title {
                        font-weight: bold; /* 굵은 글씨 */
                        color : #ffffff;
                        font-size: 17px; /* 제목 크기 */
                        margin-bottom: 8px; /* 제목 아래 여백 */
                        display: block; /* 블록 레벨 요소 */
                    }
                    .train-metrics {
                        display: flex; /* 가로 정렬 */
                        justify-content: space-around; /* 요소를 공간에 균등하게 분배 */
                    }
                    .metric {
                        text-align: center; /* 가운데 정렬 */
                    }
                    .metric-title {
                        font-weight: bold; /* 굵은 글씨 */
                        margin-bottom: 5px; /* 아래쪽 여백 */
                        color :#ffffff;
                        font-size: 13px;
                    }
                    .metric-value {
                        font-size: 15px; /* 크기 조정 */
                        color :#ffffff;
                    }
                    .train-number {
                        color: #ffffff; /* 흰색 글씨 */
                        font-size: 15px;
                    }
                    </style>

                    <div class="train-section">
                        <div class="train-title">접근차량</div>
                        <div class="train-number">열차 번호: KTX-133</div>
                        <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EA%B8%B0%EC%B0%A8%EC%B5%9C%EC%A2%85.png?_xsrf=2%7C0e3e6c52%7C422d2d71a416b56c278b7c7591d926ef%7C1704801015" alt="Train Image" style="width: 100%; height: auto; border-radius: 5px; margin-top: 10px;"/> <!-- 이미지 경로 확인 필요 -->
                        <div class="train-metrics">
                            <div class="metric">
                                <div class="metric-title">남은 시간</div>
                                <div class="metric-value">15분 0초</div>
                            </div>
                            <div class="metric">
                                <div class="metric-title">현재 속력</div>
                                <div class="metric-value">281km/h</div>
                            </div>
                            <div class="metric">
                                <div class="metric-title">현재 위치</div>
                                <div class="metric-value">광명역</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ----------------------------------------------------------------------------------------------------------------        
            #         # 페이지를 매 1초마다 자동으로 새로고침
            #         refresh_interval = 1  # 초 단위

            #         # 세션 상태 초기화
            #         if 'remaining_seconds' not in st.session_state:
            #             st.session_state.remaining_seconds = 15 * 60  # 15분
            #         if 'current_speed' not in st.session_state:
            #             st.session_state.current_speed = np.random.randint(275, 285)  # 초기 속도 설정

            #         # 남은 시간과 속력 업데이트
            #         st.session_state.remaining_seconds = max(st.session_state.remaining_seconds - refresh_interval, 0)
            #         if st.session_state.remaining_seconds == 0:
            #             st.session_state.remaining_seconds = 15 * 60  # 타이머 리셋

            #         # 임의로 속력 변화
            #         st.session_state.current_speed = np.random.randint(275, 285)

            #         # 남은 시간을 분과 초로 변환
            #         minutes, seconds = divmod(st.session_state.remaining_seconds, 60)

            #         # 메트릭 표시
            #         col1, col2, col3 = st.columns(3)
            #         with col1:
            #             st.metric("남은 시간", f"{minutes}분 {seconds}초")
            #         with col2:
            #             st.metric("현재 속력", f"{st.session_state.current_speed}km/h")
            #         with col3:
            #             st.metric("현재 위치", "오송역")

            # ----------------------------------------------------------------------------------------------------------------       

                st.markdown("""
                        <style>
                            .background-container {
                                background-color: #555555; /* 섹션 배경색 */
                                padding: 15px; /* 내부 여백 */
                                margin-bottom: 3px; /* 다음 콘텐츠와의 간격 */
                                color: white; /* 텍스트 색상 */
                            }
                            .st-title {
                                font-weight: bold; /* 굵은 글씨 */
                                color : #ffffff;
                                font-size: 17px; /* 제목 크기 */
                                margin-bottom: 8px; /* 제목 아래 여백 */
                                display: block; /* 블록 레벨 요소 */
                            }
                            .status-container {
                                display: flex;
                                flex-wrap: wrap;
                                justify-content: space-between;
                            }
                            .status-button {
                                flex-basis: 24%;
                                padding: 10px;
                                margin-bottom: 10px;
                                text-align: center;
                                background-color: #f0f0f0;
                                border: 1px solid #ccc;
                                border-radius: 4px;
                            }
                            .status-button:hover {
                                background-color: #e0e0e0;
                            }
                            .status-title {
                                font-weight: bold;
                                margin-bottom: 5px;
                                font-size: 13px;
                                color: #333;
                            }
                            .status-text {
                                color: #555;
                                font-size: 13px;
                            }
                            /* 새로운 스타일 */
                            .green-status .status-text {
                                font-weight: bold;
                                color: #005BAC;
                                font-size: 13px;
                            }
                        </style>
                        <div class='background-container'>
                            <div class="st-title">시설물 상태정보</div>
                            <div class="status-container">
                                <div class="status-button green-status"> <!-- 첫 번째 버튼에 클래스 추가 -->
                                    <div class="status-title">선로</div>
                                    <div class="status-text">이촌</div>
                                    <div class="status-text">정비중</div>
                                </div>
                                <div class="status-button">
                                    <div class="status-title">전선</div>
                                    <div class="status-text">이상</div>
                                    <div class="status-text">없음</div>
                                </div>
                                <div class="status-button">
                                    <div class="status-title">신호기</div>
                                    <div class="status-text">이상</div>
                                    <div class="status-text">없음</div>
                                </div>
                                <div class="status-button green-status"> <!-- 네 번째 버튼에 클래스 추가 -->
                                    <div class="status-title">차량</div>
                                    <div class="status-text">34347</div>
                                    <div class="status-text">수리 중</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)


            # ----------------------------------------------------------------------------------------------------------------

            with main_col:
                workers_data = create_initial_data()
                workers_data = update_data(workers_data)
                display_fullscreen_alert()  # 경고 메시지 표시

                with st.container():
                    # CSS 스타일을 적용하기 위한 st.markdown()
                    st.markdown("""
                        <style>
                            .location-section {
                                background-color: #555555; /* 연한 회색 */
                                padding: 10px; /* 안쪽 여백 */
                                display: block; /* 블록 레벨 요소 */
                            }
                            .location-title {
                                font-weight: bold; /* 굵은 글씨 */
                                color : #ffffff;
                                font-size: 17px; /* 제목 크기 */
                                display: block; /* 블록 레벨 요소 */
                            }
                            .deckgl-canvas {
                                height: 700px !important;
                            }
                        </style>
                        <div class='location-section'>
                            <div class="location-title">작업자 위치</div>
                    """, unsafe_allow_html=True)

                # 지도 레이어 설정
                    layer = pdk.Layer(
                        "ScatterplotLayer",
                        workers_data,
                        get_position=['longitude', 'latitude'],
                        get_color='color',
                        get_radius=8,
                        pickable=True,
                        extruded=True,
                    )

                    # 뷰 상태 설정
                    view_state = pdk.ViewState(
                        latitude=37.611294,
                        longitude=126.830462,
                        zoom=16.2,
                        pitch=0,
                    )

                    # 지도 생성
                    r = pdk.Deck(
                        layers=[layer],
                        initial_view_state=view_state,
                        map_style='mapbox://styles/mapbox/satellite-v9',
                        tooltip={
                            'html': ('<b>작업자명:</b> {worker_id}<br>'
                                     '<b>작업:</b> {task}<br>'
                                     '<b>근무 시간:</b> {start_time} - {end_time}<br>'
                                     '<b>현재 상태:</b> {status}'),
                            'style': {
                                'backgroundColor': 'white',
                                'color': 'black',
                                'fontSize': '13px',
                                'fontWeight': 'bold',
                                'padding': '10px',
                            }})

                    st.pydeck_chart(r)
                    st.markdown(
                        """
                        <style>
                        div.stButton > button:first-child {
                            display: flex;
                            margin-left: auto; 
                            margin-right: 0;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )


                    # 업무 시작 버튼
                    if st.button('관제'):
                        start_work()


            # ----------------------------------------------------------------------------------------------------------------

            # 오른쪽 섹션 컴포넌트
                # with right_col:
                #     with st.container():
                #         st.markdown("""
                #         <style>
                #         .worker-section {
                #             background-color: #555555; 
                #             padding: 20px;
                #             margin-bottom: 20px;
                #         }
                #         .columns-container {
                #             display: flex;
                #         }
                #         .column {
                #             flex: 1; /* 칼럼에 자동으로 공간을 나누어 줍니다. */
                #             padding: 10px;
                #         }
                #         .worker-title {
                #             font-weight: bold;
                #             font-size: 1.25em;
                #             margin-bottom: 10px;
                #             color: white; 
                #         }
                #         .metric-label {
                #             color: white !important; 
                #         }
                #         .metric-value {
                #             color: white !important; 
                #         }
                #         .expander-title {
                #             color: white !important; 
                #         }
                #         .expander-content {
                #             color: white; 
                #         }
                #         </style>
                #         <div class="worker-section">
                #             <h2 class="worker-title">작업자 현황</h2>
                #             <div class="columns-container">
                #                 <div class="column">
                #                     <div class="metric-label">잔류인원</div>
                #                     <div class="metric-value">211/250</div>
                #                 </div>
                #                 <div class="column">
                #                     <div class="expander-title">선로 8명</div>
                #                     <div class="expander-content">선로 관련 상세 정보</div>
                #                     <div class="expander-title">전선 6명</div>
                #                     <div class="expander-content">전선 관련 상세 정보</div>
                #                     <div class="expander-title">신호기 0명</div>
                #                     <div class="expander-content">신호기 관련 상세 정보</div>
                #                     <div class="expander-title">열차 14명</div>
                #                     <div class="expander-content">열차 관련 상세 정보</div>
                #                 </div>
                #             </div>
                #         </div>
                #         """, unsafe_allow_html=True)

                with right_col:
                    st.markdown("""
                    <style>
                        .back-container {
                            background-color: #555555; /* 전체 배경색 설정 */
                            color: white;
                            padding: 15px;
                            margin-bottom: 3px; /* 아래쪽 여백 추가 */
                        }

                        .dashboard-container {
                            display: flex;
                            flex-direction: row;
                            gap: 10px; /* 내부 요소 사이의 간격 */
                        }

                        .metric-container {
                            flex: 1; /* flex-basis를 1로 설정하여 비율에 따라 크기 조정 */
                            background-color: #555555;
                            border: 2px solid #ffffff; /* 흰색 테두리 추가 */
                            border-radius: 5px;
                            font-size: 15px;
                            font-weight: bold;
                            padding: 20px;
                            text-align: center;
                        }

                        .cards-container {
                            flex: 2; /* flex-basis를 2로 설정하여 비율에 따라 크기 조정 */
                            display: flex;
                            flex-direction: column;
                            gap: 5px; /* 카드 사이의 여백을 늘림 */
                        }

                        .card-container {
                            border: 2px solid #999;
                            border-radius: 5px;
                            background-color: #555555; /* 카드 배경색 변경 */
                            color: white;
                            padding: 10px;
                            font-size: 13px;
                        }

                        /* 특정 카드의 테두리 색상을 파란색으로 설정 */
                        .card-container:nth-of-type(1), 
                        .card-container:nth-of-type(2), 
                        .card-container:nth-of-type(4) {
                            border-color: #005BAC; /* 파란색 테두리 */
                            background-color: #005BAC
                        }

                        .worker-title {
                            font-weight: bold; /* 굵은 글씨 */
                            color : #ffffff;
                            font-size: 17px; /* 제목 크기 */
                            margin-bottom: 8px; /* 제목 아래 여백 */
                            display: block; /* 블록 레벨 요소 */
                        }

                        .custom-content {
                            display: none; /* 기본적으로 숨겨져 있음 */
                            padding: 10px;
                            list-style: none; /* 리스트 마커 제거 */
                            margin: 0; /* 리스트 마진 제거 */
                            padding-left: 20px;/* 들여쓰기 추가 */
                            font-size: 11px;
                        }

                        /* 클릭했을 때 내용을 표시합니다 */
                        .card-container:hover .custom-content {
                            display: block; /* 호버 시에 표시 */
                            font-size: 11px;
                        }
                        .custom-content ul li {
                            font-size: 11px; /* 여기에서 원하는 글자 크기로 조절하세요 */
                            /* 추가적인 스타일링이 필요하면 여기에 코드를 추가하세요 */
                        }

                    </style>

                    <div class="back-container">
                        <div class="worker-title">작업자 현황</div>
                        <div class="dashboard-container">
                            <div class="metric-container">잔류인원 20/250</div>
                            <div class="cards-container">
                                <div class="card-container">
                                    <div class="cardia">선로 8명</div>
                                    <div class="custom-content">
                                        <ul>
                                            <li>박준형</li>
                                            <li>김태우</li>
                                            <li>정철민</li>
                                            <li>한상철</li>
                                            <li>이형석</li>
                                            <li>조민수</li>
                                            <li>최병호</li>
                                            <li>윤대현</li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="card-container">
                                    <div class="cardia">전선 6명</div>
                                    <div class="custom-content">
                                        <ul>
                                            <li>서정국</li>
                                            <li>김준호</li>
                                            <li>이상민</li>
                                            <li>장성호</li>
                                            <li>유병철</li>
                                            <li>손진호</li>
                                         </ul>
                                    </div>
                                </div>
                                <div class="card-container">
                                    <div class="cardia">신호기 0명</div>
                                    <div class="custom-content">
                                        <ul>
                                            <li>신호기 관련 상세 정보</li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="card-container">
                                    <div class="cardia">열차 6명</div>
                                    <div class="custom-content">
                                        <ul>
                                            <li>김도현</li>
                                            <li>박기영</li>
                                            <li>이준석</li>
                                            <li>정태민</li>
                                            <li>최준표</li>
                                            <li>김성태</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)


        # ----------------------------------------------------------------------------------------------------------------
                    first_card_style = "border-color: #3432B2; background-color: #364656;"

                    st.markdown("""
                    <style>
                        .background-container {
                            background-color: #555555; /* 섹션 배경색 */
                            padding: 15px; /* 내부 여백 */
                            margin-bottom: 3px; /* 다음 콘텐츠와의 간격 */
                            color: white; /* 텍스트 색상 */
                        }
                        .section-title {
                            font-weight: bold; /* 굵은 글씨 */
                            color : #ffffff;
                            font-size: 17px; /* 제목 크기 */
                            margin-bottom: 8px; /* 제목 아래 여백 */
                            display: block; /* 블록 레벨 요소 */
                        }

                        .card {
                            display: flex;
                            flex-direction: row;
                            align-items: center;
                            justify-content: space-between;
                            padding: 16px;
                            background-color: #555555; /* 카드 배경색 */
                            border-radius: 8px;
                            border: 2px solid #ccc; /* 카드 테두리 */
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* 카드 그림자 */
                            color: white;
                            margin-bottom: 10px; /* 카드 간 여백 */
                        }

                        .card-content {
                            display: flex;
                            flex-direction: column;
                        }
                        .card-title {
                            font-size: 13px;
                            font-weight: bold;
                            color: white;
                        }
                        .card-subtitle {
                            font-size: 11px;
                            color: white;
                        }
                        .card-icon {
                            width: 50px; /* 아이콘 크기 */
                            height: 50px;
                        }
                        .first-card {
                            border-color: #005BAC !important; /* 첫 번째 카드 테두리 색상 */
                            background-color: #005BAC !important; /* 첫 번째 카드 배경색 */
                        }
                    </style>

                    <div class='background-container'>
                        <div class='section-title'>작업현황</div>
                        <!-- 첫 번째 카드 -->
                        <div class="card first-card">
                            <div class="card-content">
                                <div class="card-title">이촌역 하부_선로 정비 작업</div>
                                <div class="card-subtitle">예상 소요 시간 |</div>
                                <div class="card-subtitle">2024.01.12 13:00 - 15:30</div>
                            </div>
                            <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EC%84%A0%EB%A1%9C.png?_xsrf=2%7C0e3e6c52%7C422d2d71a416b56c278b7c7591d926ef%7C1704801015" alt="Icon" class="card-icon">
                        </div>
                        <!-- 두 번째 카드 -->
                        <div class="card">
                            <div class="card-content">
                                <div class="card-title">행신역 하부_전기 설비 작업</div>
                                <div class="card-subtitle">예상 소요 시간 |</div>
                                <div class="card-subtitle">2024.01.12 17:00 - 19:00</div>
                            </div>
                            <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EC%A0%84%EA%B8%B0.png?_xsrf=2%7C0e3e6c52%7C422d2d71a416b56c278b7c7591d926ef%7C1704801015" alt="Icon" class="card-icon">
                        </div>
                        <!-- 세 번째 카드 -->
                        <div class="card">
                            <div class="card-content">
                                <div class="card-title">광명역 하부_위치 정비 작업</div>
                                <div class="card-subtitle">예상 소요 시간 |</div>
                                <div class="card-subtitle">2024.01.12 19:30 - 21:30</div>
                            </div>
                            <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EC%B0%A8%EB%9F%89.png?_xsrf=2%7C0e3e6c52%7C422d2d71a416b56c278b7c7591d926ef%7C1704801015" alt="Icon" class="card-icon">
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ----------------------------------------------------------------------------------------------------------------



        update_state()
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################

#elif (component1 == 1):
with tab2:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #333333;
        }
        /* Remove padding and margin from the main block */
        .block-container {
                padding-top: 1rem; /* 위에 패딩 */
                padding-right: 1rem; /* 오른쪽 패딩 */
                padding-left: 1rem; /* 왼쪽 패딩 */
                padding-bottom: 1rem; /* 아래 패딩 */
            }

            /* 스트림릿의 칼럼 사이 간격 조정 */
            .st-cx {
                margin: 0; /* 외부 여백 제거 */
            }

            /* 칼럼 내부의 패딩 조정 */
            .st-cc {
                padding:0.5rem; /* 좌우 패딩 */
            }
            .st-de { 
                margin-left: 0px; 
                margin-right: 0px; 
            }
            /* 칼럼 내부의 패딩 조정 */
            .st-cy {
                padding: 8px; /* 상하좌우 패딩을 8px로 설정 */
            }
        </style>
        </style>
        """,
        unsafe_allow_html=True
    )


    # 상단바 스타일과 컴포넌트 정의
    st.markdown("""

    <style>

    .header {
        background-color:black;
        color: white;
        padding: 10px 0px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .logo {
        flex-grow: 2;
        display: flex;
        align-items: center;
    }
    .logo > img {
        margin-right: 20px;
    }

    .logo-text {
        display: flex;
        align-items: center;
        font-size: 24px; /* 텍스트 크기 증가 */
        font-weight: bold;
        margin-right: 20px; /* 오른쪽 여백 추가 */
        color : #eeeeee;
    }

    .search-box {
        display: flex;
        justify-content: right;
    }

    .search-input {
        background-color: #999999; /* 검색창 배경색 */
        color: white; /* 검색창 텍스트 색상 */
        margin: 0px 10px;
        padding: 10px 15px; /* 검색창 내부 패딩 */
        border-radius: 20px; /* 검색창 라운드 값 */
        border: 1px solid #004165; /* 검색창 테두리 색상 */
        outline: none; /* 클릭 시 발생하는 아웃라인 제거 */
    }
    .search-input::placeholder {
        color: white; /* 플레이스홀더 텍스트 색상을 흰색으로 설정 */
        opacity: 1; /* 플레이스홀더 텍스트의 불투명도를 100%로 설정 */
    }
    .notifications {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        margin-left: 20px; /* 왼쪽 여백 추가 */
        font-size: 12px;
    }
    .clock {
        display: flex;
        align-items: center;
        margin-left: 20px; /* 왼쪽 여백 추가 */
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 상단바 컴포넌트
    st.markdown("""
    <div class="header">
        <div class="logo">
            <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EB%A1%9C%EA%B3%A0.png?_xsrf=2%7Ce9d7a21b%7C50c7ca14a3dd56ebb3a431afcbbaa867%7C1704802869" height="40"/>
            <div class="logo-text">CCTV</div>
        </div>
        <div class="search-box">
            <input class="search-input" type="text" placeholder="🔍 차량 번호 입력" />
            <input class="search-input" type="text" placeholder="🔍 노선, 정류장 입력" />
        </div>
        <div class="notifications">
            🔔 이벤트 12건
        </div>
        <div class="clock" id="clock">
            <!-- 시간 표시 -->
        </div>
    </div>
    """, unsafe_allow_html=True)



    # --------------------------------------------------------------------------------------------------

    # /* 버튼 스타일 */
    #             .custom-button {
    #                 margin: 10px;
    #                 padding: 10px 20px;
    #                 border: none;
    #                 background-color: grey;
    #                 color: white;
    #                 border-radius: 5px;
    #                 cursor: pointer;
    #             } 
    # st.markdown("""
    #             <div class="button-container">
    #                 <button class="custom-button">+</button>
    #                 <button class="custom-button">-</button>
    #             </div>
    #         """, unsafe_allow_html=True)       
    #------------------------------------------------------------------------------------------------
    def add_custom_css():
        st.markdown("""
        <style>
        .tab-button {
            background-color: black;
            color: white;
            padding: 10px;
            border: none;
            margin: 0px; /* Remove space between buttons */
            cursor: pointer;
            width: 100%; /* Set the width of buttons to be equal */
        }
        .tab-button:hover {
            background-color: #555;
        }
        /* Remove gap between columns */
        .column {
            padding: 0px !important;
        }
        </style>
        """, unsafe_allow_html=True)

    add_custom_css()

    # 화면 분할 설정 - 왼쪽에 탭, 오른쪽에 파일 내용
    left_column, right_column = st.columns([1, 18])

    # 왼쪽 컬럼에 탭 버튼 배치
    with left_column:
        tab_buttons = {
            '메인': '메인',
            'CCTV': 'CCTV',
            '분석': '분석'
        }
        for tab_key, tab_value in tab_buttons.items():
            button_html = f"<button class='tab-button' onclick='window.location.href=\"?current_tab={tab_key}\"'>{tab_value}</button>"
            st.markdown(button_html, unsafe_allow_html=True)




    # 오른쪽 컬럼에 파일 내용 표시
    with right_column:
    # 넓은 레이아웃 설정



        # 하단 CCTV 피드
        slider_spacing = "3px"

        st.markdown("""
            <style>
                .cctv-container {
                    background-color: #333333;
                    border: 2px solid #FFFFFF; /* 초기 테두리는 흰색 */
                    border-radius: 10px;
                    margin-bottom: 20px;
                    overflow: hidden;
                    display: flex;
                }

                .cctv-container_alert {
                    background-color: #333333;

                    border: 2px solid #FFFFFF; /* 초기 테두리 색상: 흰색 */
                    animation: blink 1s linear infinite; /* 애니메이션 적용 */
                    animation-delay: 10s; /* 10초 후 애니메이션 시작 */
                    border-radius: 10px;
                    margin-bottom: 20px;
                    overflow: hidden;
                    display: flex;
                }
                @keyframes blink {
                    0% {
                        border-color: #FFFF00; /* 시작 색상: 노란색 */
                    }
                    50% {
                        border-color: transparent; /* 50% 지점: 테두리 투명화 */
                    }
                    100% {
                        border-color: #FFFF00; /* 종료 색상: 노란색 */
                    }
                }
                .blinking-cctv {
                    animation: blink 1s linear infinite; /* 애니메이션 적용 */
                }

                }
                .cctv-controls, .cctv-feed {
                    padding: 10px;
                    color: white;
                }
                .cctv-controls {
                    flex: 2; /* 1:5 비율의 좌측 부분 */
                    padding: 10px;
                }
                .cctv-feed {
                    flex: 6; /* 1:5 비율의 우측 부분 */
                    width: 100%;
                    height: auto;
                }

                /* 제목 글자 크기를 조정합니다. */
                .stSubheader, .stMarkdown {
                    font-size: 10px !important;
                    color: white !important;
                }
                /* 슬라이더 라벨의 글씨 색상을 변경합니다. */
                .stSlider label {
                    color: white !important;
                    font-size: 10px
                }
                /* 슬라이더 핸들과 트랙의 색상을 변경할 수 있습니다. */
                .st-bd, .st-eg {
                    background-color: #FF4B4B !important;
                }
                /* 슬라이더 간격을 줄입니다. */
                .stSlider {
                    margin-bottom: 3px !important;
                }
                /* 슬라이더 값 표시를 숨깁니다. */
                .stSlider .st-ef {
                    visibility: hidden;
                }
                /* 컬럼의 최소 높이 설정 */
                .st-cb, .st-cc {
                    min-height: 25px;
                }
                .cctv-controls div {
                    margin-bottom: 10px; /* 각 컨트롤 요소의 하단 여백 */
                }

                .cctv-controls label {
                    display: block; /* 라벨을 블록 요소로 만들어 줄 바꿈 */
                    color: white;
                    font-size: 14px; /* 라벨의 글자 크기 */
                    margin-bottom: 5px; /* 라벨과 슬라이더 사이의 여백 */
                }

                .cctv-controls input[type=range] {
                    width: 100%; /* 슬라이더의 길이 */
                }
            </style>
        """,
            unsafe_allow_html=True
        )

        # 각 CCTV 블록을 만드는 함수
        def create_cctv_block(cctv_number, video_url):
            cctv_id = f"cctv-{cctv_number}"
            if cctv_number == 4:

                st.markdown(f"""
                <div class="cctv-container_alert">
                    <div class="cctv-controls">
                        <h2 style="font-size: 15px; margin-bottom: 5px; color: white;">Control Panel {cctv_number}</h2>
                        <label for="zoom_{cctv_number}">Zoom</label>
                        <input type="range" id="zoom_{cctv_number}" min="0" max="10" value="5">
                        <label for="focus_{cctv_number}">Focus</label>
                        <input type="range" id="focus_{cctv_number}" min="0" max="100" value="50">
                        <label for="step_{cctv_number}">Step</label>
                        <input type="range" id="step_{cctv_number}" min="0" max="10" value="1">
                    </div>
                    <div class="cctv-feed">
                        <h2 style="font-size: 14px; margin-bottom: 5px; color: white;">CCTV Feed {cctv_number}</h2>
                        <video autoplay loop controls style="width: 100%; height: auto; max-height: 100%;">
                            <source src="{video_url}" type="video/mp4">
                        </video>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="cctv-container">
                    <div class="cctv-controls">
                        <h2 style="font-size: 18px; margin-bottom: 5px; color: white;">Control Panel {cctv_number}</h2>
                        <label for="zoom_{cctv_number}">Zoom</label>
                        <input type="range" id="zoom_{cctv_number}" min="0" max="10" value="8">
                        <label for="focus_{cctv_number}">Focus</label>
                        <input type="range" id="focus_{cctv_number}" min="0" max="100" value="40">
                        <label for="step_{cctv_number}">Step</label>
                        <input type="range" id="step_{cctv_number}" min="0" max="10" value="6">
                    </div>
                    <div class="cctv-feed">
                        <h2 style="font-size: 18px; margin-bottom: 5px; color: white;">CCTV Feed {cctv_number}</h2>
                        <video autoplay loop controls style="width: 100%; height: auto; max-height: 100%;">
                            <source src="{video_url}" type="video/mp4">
                        </video>
                    </div>
                </div>
                """, unsafe_allow_html=True)




        # CCTV 피드와 컨트롤 패널 레이아웃 구성'
        # html 연계 시 copy download link
        cctv_col1, cctv_col2 = st.columns(2)
        with cctv_col1:
            create_cctv_block(1, 'http://localhost:8888/files/BigProject/bigproject_dashboard/CCTV1.mp4?_xsrf=2%7Cd90943e7%7C393b8f80a9c011b8033e51ffbe31e2d9%7C1704793804')
        with cctv_col2:
            create_cctv_block(2, 'http://localhost:8888/files/BigProject/bigproject_dashboard/CCTV2.mp4?_xsrf=2%7Cd90943e7%7C393b8f80a9c011b8033e51ffbe31e2d9%7C1704793804')


        # 두 번째 행의 CCTV 피드들
        # html 연계 시 copy download link
        cctv_col3, cctv_col4 = st.columns(2)
        with cctv_col3:
            create_cctv_block(3, 'http://localhost:8888/files/BigProject/bigproject_dashboard/CCTV3.mp4?_xsrf=2%7Cd90943e7%7C393b8f80a9c011b8033e51ffbe31e2d9%7C1704793804')
        with cctv_col4:
            create_cctv_block(4, 'http://localhost:8888/files/BigProject/bigproject_dashboard/CCTV4.mp4?_xsrf=2%7Cd90943e7%7C393b8f80a9c011b8033e51ffbe31e2d9%7C1704793804')


        
################################################################
#################################################################
################################################################
#################################################################

with tab3:
#else:   

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #333333;
        }
        /* Remove padding and margin from the main block */
        .block-container {
                padding-top: 1rem; /* 위에 패딩 */
                padding-right: 1rem; /* 오른쪽 패딩 */
                padding-left: 1rem; /* 왼쪽 패딩 */
                padding-bottom: 1rem; /* 아래 패딩 */
            }

            /* 스트림릿의 칼럼 사이 간격 조정 */
            .st-cx {
                margin: 0; /* 외부 여백 제거 */
            }

            /* 칼럼 내부의 패딩 조정 */
            .st-cc {
                padding:0.5rem; /* 좌우 패딩 */
            }
            .st-de { 
                margin-left: 0px; 
                margin-right: 0px; 
            }
            /* 칼럼 내부의 패딩 조정 */
            .st-cy {
                padding: 8px; /* 상하좌우 패딩을 8px로 설정 */
            }
        </style>
        </style>
        """,
        unsafe_allow_html=True
    )


    # def display_fullscreen_alert():
    #     # 경고창을 위한 컨테이너 생성
    #     alert_container = st.empty()

    #     # 경고 메시지 표시
    #     with alert_container:
    #         st.markdown(
    #             """
    #             <style>
    #             .overlay {
    #                 position: fixed;
    #                 display: flex;
    #                 justify-content: center;
    #                 align-items: center;
    #                 top: 0;
    #                 left: 0;
    #                 right: 0;
    #                 bottom: 0;
    #                 background-color: rgba(0,0,0,0.5);
    #                 z-index: 999;
    #                 animation: blinker 3s linear 3;
    #             }
    #             @keyframes blinker {
    #                 50% { opacity: 0; }
    #             }
    #             .alert-box {
    #                 background-color: #ffcc00;
    #                 color: black;
    #                 padding: 20px;
    #                 border-radius: 5px;
    #                 box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    #                 text-align: center;
    #                 max-width: 500px;
    #             }
    #             </style>
    #             <div class="overlay">
    #                 <div class="alert-box">
    #                     <strong>경고:</strong> 주의가 필요한 상황이 감지되었습니다.
    #                 </div>
    #             </div>
    #             """,
    #             unsafe_allow_html=True
    #         )
    #     time.sleep(7)  # 7초간 대기
    #     alert_container.empty()  # 경고창 컨테이너 비우기



    # 상단바 스타일과 컴포넌트 정의
    st.markdown("""

    <style>

    .header {
        background-color:black;
        color: white;
        padding: 10px 0px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .logo {
        flex-grow: 2;
        display: flex;
        align-items: center;
    }
    .logo > img {
        margin-right: 20px;
    }

    .logo-text {
        display: flex;
        align-items: center;
        font-size: 24px; /* 텍스트 크기 증가 */
        font-weight: bold;
        margin-right: 20px; /* 오른쪽 여백 추가 */
        color : #eeeeee;
    }

    .search-box {
        display: flex;
        justify-content: right;
    }

    .search-input {
        background-color: #999999; /* 검색창 배경색 */
        color: white; /* 검색창 텍스트 색상 */
        margin: 0px 10px;
        padding: 10px 15px; /* 검색창 내부 패딩 */
        border-radius: 20px; /* 검색창 라운드 값 */
        border: 1px solid #004165; /* 검색창 테두리 색상 */
        outline: none; /* 클릭 시 발생하는 아웃라인 제거 */
    }
    .search-input::placeholder {
        color: white; /* 플레이스홀더 텍스트 색상을 흰색으로 설정 */
        opacity: 1; /* 플레이스홀더 텍스트의 불투명도를 100%로 설정 */
    }
    .notifications {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        margin-left: 20px; /* 왼쪽 여백 추가 */
        font-size: 12px;
    }
    .clock {
        display: flex;
        align-items: center;
        margin-left: 20px; /* 왼쪽 여백 추가 */
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 상단바 컴포넌트
    st.markdown("""
    <div class="header">
        <div class="logo">
            <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EB%A1%9C%EA%B3%A0.png?_xsrf=2%7Ce9d7a21b%7C50c7ca14a3dd56ebb3a431afcbbaa867%7C1704802869" height="40"/>
            <div class="logo-text">CCTV</div>
        </div>
        <div class="search-box">
            <input class="search-input" type="text" placeholder="🔍 차량 번호 입력" />
            <input class="search-input" type="text" placeholder="🔍 노선, 정류장 입력" />
        </div>
        <div class="notifications">
            🔔 이벤트 12건
        </div>
        <div class="clock" id="clock">
            <!-- 시간 표시 -->
        </div>
    </div>
    """, unsafe_allow_html=True)


    #------------------------------------------------------------------------------------------------

    # 하단 CCTV 피드
    slider_spacing = "3px"
    # 스타일 정의
    st.markdown("""
        <style>
            .cctv-container {
                background-color: #333333;
                border: 2px solid #AAAAAA; /* 초기 테두리는 흰색 */
                border-radius: 10px;
                margin-bottom: 20px;
                overflow: hidden;
                display: flex;
            }
            .cctv-controls, .cctv-feed {
                padding: 10px;
                color: white;
            }
            .cctv-controls {
                flex: 2; /* 1:5 비율의 좌측 부분 */
            }
            .cctv-feed {
                flex: 6; /* 1:5 비율의 우측 부분 */
                width: 100%;
                height: auto;
            }

            /* 제목 글자 크기를 조정합니다. */
            .stSubheader, .stMarkdown {
                font-size: 10px !important;
                color: white !important;
            }
            /* 슬라이더 라벨의 글씨 색상을 변경합니다. */
            .stSlider label {
                color: white !important;
                font-size: 10px
            }
            /* 슬라이더 핸들과 트랙의 색상을 변경할 수 있습니다. */
            .st-bd, .st-eg {
                background-color: #FF4B4B !important;
            }
            /* 슬라이더 간격을 줄입니다. */
            .stSlider {
                margin-bottom: 3px !important;
            }
            /* 슬라이더 값 표시를 숨깁니다. */
            .stSlider .st-ef {
                visibility: hidden;
            }
            /* 컬럼의 최소 높이 설정 */
            .st-cb, .st-cc {
                min-height: 25px;
            }
            .cctv-controls div {
                margin-bottom: 10px; /* 각 컨트롤 요소의 하단 여백 */
            }

            .cctv-controls label {
                display: block; /* 라벨을 블록 요소로 만들어 줄 바꿈 */
                color: white;
                font-size: 14px; /* 라벨의 글자 크기 */
                margin-bottom: 5px; /* 라벨과 슬라이더 사이의 여백 */
            }

            .cctv-controls input[type=range] {
                width: 100%; /* 슬라이더의 길이 */
            }
        </style>
    """,
        unsafe_allow_html=True
    )

    # 각 CCTV 블록을 만드는 함수
    st.markdown(f"""
        <div class="cctv-container">
            <div class="cctv-controls">
                <h2 style="font-size: 18px; margin-bottom: 5px; color: white;">Control Panel</h2>
                <div>
                    <label for="zoom">Zoom</label>
                    <input type="range" id="zoom" min="0" max="10" value="8">
                </div>
                <div>
                    <label for="focus">Focus</label>
                    <input type="range" id="focus" min="0" max="100" value="40">
                </div>
                <div>
                    <label for="step">Step</label>
                    <input type="range" id="step" min="0" max="10" value="6">
                </div>
            </div>
            <div class="cctv-feed">
                <h2 style="font-size: 18px; margin-bottom: 5px; color: white;">CCTV Feed</h2>
                <video autoplay loop controls style="width: 100%; height: auto; max-height: 100%;">
                    <source src="http://localhost:8888/files/BigProject/bigproject_dashboard/video2.mp4?_xsrf=2%7C9c1195d2%7C757c1df7b8ecc23745d841df416c8be4%7C1704800877" type="video/mp4">
                </video>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # time.sleep(10)
    # display_fullscreen_alert()   
        
        
        
        
        
        
