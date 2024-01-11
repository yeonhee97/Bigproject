
import streamlit as st
import pydeck as pdk
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta
from st_tabs import TabBar
import plotly.express as px
import random
st.set_page_config(layout="wide")

for i in range(2):
    st.columns(1)

component1=  TabBar(tabs=['메인화면','CCTV','CCTV화면','분석'],default=0,background = "#000000",color="#FFFFFF",
                    activeColor="#005BAC",fontSize="15px")

def display():
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
        """,
        unsafe_allow_html=True)

        
if (component1 == 0):

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

 #------------------함수-----------------------------------------------------   
    if 'vehicle_time' not in st.session_state:
        st.session_state.vehicle_time = 60  # 예: 60초로 시작
    
    # -----------------------------------------------------------------------------------------------------
    # 스타일을 위한 CSS 추가

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



    # UI 구성
    # display_time()
    display()
    
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
                <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EB%A1%9C%EA%B3%A0.png?_xsrf=2%7Cd3664c29%7C327bdf892b15e2ab5722f8f18c538940%7C1704906402" height="40"/>
                <div class="logo-text">수도권 철도 차량기지 관제센터</div>
            </div>
            <div class="search-box">
                <input class="search-input" type="text" size="20" placeholder="🔍 차량 번호 입력" />
                <input class="search-input" type="text" size="20" placeholder="🔍 역 이름 입력" />
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
                # speed_box =  st.empty()
                # time_box =  st.empty()
                # sec_now = 
                # while True:        
                #     random_number = random.randint(275, 285)  # 랜덤 숫자 생성
                #     speed_box.text(f'{random_number}km/h')  # 박스에 숫자 출력
                #     minute = sec_now//60
                #     second = sec_now % 60
                #     time_box.text(f'{minute}분 {second}초')
                #     sec_now -= 1
                #     if sec_now == 839:
                #         break
                #     time.sleep(1)
        
                
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
                    <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EA%B8%B0%EC%B0%A8%EC%B5%9C%EC%A2%85.png?_xsrf=2%7Cb33aa785%7Cd3cea70bacfd3af651e9a8666ac7420a%7C1704934306" alt="Train Image" style="width: 100%; height: auto; border-radius: 5px; margin-top: 10px;"/> <!-- 이미지 경로 확인 필요 -->
                </div>
                """, unsafe_allow_html=True)
                
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
                <div class="train-title">남은 시간  현재속력  현재 위치</div>
                    """, unsafe_allow_html=True)
                
                # col_t, col_s,col_l = st.columns(3)
                # with col_t:
                #     time_box.text(f'{minute}분 {second}초')
                # with col_s:
                #     speed_box.text(f'{random_number}km/h')
                
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
                        <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EC%84%A0%EB%A1%9C.png?_xsrf=2%7Cb33aa785%7Cd3cea70bacfd3af651e9a8666ac7420a%7C1704934306" alt="Icon" class="card-icon">
                    </div>
                    <!-- 두 번째 카드 -->
                    <div class="card">
                        <div class="card-content">
                            <div class="card-title">행신역 하부_전기 설비 작업</div>
                            <div class="card-subtitle">예상 소요 시간 |</div>
                            <div class="card-subtitle">2024.01.12 17:00 - 19:00</div>
                        </div>
                        <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EC%A0%84%EA%B8%B0.png?_xsrf=2%7Cb33aa785%7Cd3cea70bacfd3af651e9a8666ac7420a%7C1704934306" alt="Icon" class="card-icon">
                    </div>
                    <!-- 세 번째 카드 -->
                    <div class="card">
                        <div class="card-content">
                            <div class="card-title">광명역 하부_위치 정비 작업</div>
                            <div class="card-subtitle">예상 소요 시간 |</div>
                            <div class="card-subtitle">2024.01.12 19:30 - 21:30</div>
                        </div>
                        <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EC%B0%A8%EB%9F%89.png?_xsrf=2%7Cb33aa785%7Cd3cea70bacfd3af651e9a8666ac7420a%7C1704934306" alt="Icon" class="card-icon">
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

elif (component1 == 1):
#with tab2:
    display()

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
                <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EB%A1%9C%EA%B3%A0.png?_xsrf=2%7Cd3664c29%7C327bdf892b15e2ab5722f8f18c538940%7C1704906402" height="40"/>
                <div class="logo-text">CCTV1</div>
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
                    <h2 style="font-size: 18px; margin-bottom: 5px; color: white;">Control Panel {cctv_number}</h2>
                    <label for="zoom_{cctv_number}">Zoom</label>
                    <input type="range" id="zoom_{cctv_number}" min="0" max="10" value="5">
                    <label for="focus_{cctv_number}">Focus</label>
                    <input type="range" id="focus_{cctv_number}" min="0" max="100" value="50">
                    <label for="step_{cctv_number}">Step</label>
                    <input type="range" id="step_{cctv_number}" min="0" max="10" value="1">
                </div>
                <div class="cctv-feed">
                    <h2 style="font-size: 18px; margin-bottom: 5px; color: white;">CCTV Feed {cctv_number}</h2>
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
        create_cctv_block(1, 'http://localhost:8888/files/BigProject/bigproject_dashboard/CCTV1.mp4?_xsrf=2%7Cb33aa785%7Cd3cea70bacfd3af651e9a8666ac7420a%7C1704934306')
    with cctv_col2:
        create_cctv_block(2, 'http://localhost:8888/files/BigProject/bigproject_dashboard/CCTV2.mp4?_xsrf=2%7Cb33aa785%7Cd3cea70bacfd3af651e9a8666ac7420a%7C1704934306')
    # 두 번째 행의 CCTV 피드들
    # html 연계 시 copy download link
    cctv_col3, cctv_col4 = st.columns(2)
    with cctv_col3:
        create_cctv_block(3, 'http://localhost:8888/files/BigProject/bigproject_dashboard/CCTV3.mp4?_xsrf=2%7Cb33aa785%7Cd3cea70bacfd3af651e9a8666ac7420a%7C1704934306')
    with cctv_col4:
        create_cctv_block(4, 'http://localhost:8888/files/BigProject/bigproject_dashboard/CCTV4.mp4?_xsrf=2%7Cb33aa785%7Cd3cea70bacfd3af651e9a8666ac7420a%7C1704934306')
    
    
################################################################
#################################################################
################################################################
#################################################################

#with tab3:
elif (component1 == 2):   

    display()

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
                <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EB%A1%9C%EA%B3%A0.png?_xsrf=2%7Cd3664c29%7C327bdf892b15e2ab5722f8f18c538940%7C1704906402" height="40"/>
                <div class="logo-text">CCTV2</div>
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
                    <source src="http://localhost:8888/files/BigProject/bigproject_dashboard/video2.mp4?_xsrf=2%7Cb33aa785%7Cd3cea70bacfd3af651e9a8666ac7420a%7C1704934306" type="video/mp4">
                </video>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # time.sleep(10)
    # display_fullscreen_alert()   
        
        
######################################################################################
######################################################################################
######################################################################################
######################################################################################
     
else:
    display()
    
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
            margin-bottom:15px;
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
                <img src="http://localhost:8888/files/BigProject/bigproject_dashboard/%EB%A1%9C%EA%B3%A0.png?_xsrf=2%7Cd3664c29%7C327bdf892b15e2ab5722f8f18c538940%7C1704906402" height="40"/>
                <div class="logo-text">통계</div>
            </div>
            <div class="search-box">
                <input class="search-input" type="text" size="20" placeholder="🔍 차량 번호 입력" />
                <input class="search-input" type="text" size="20" placeholder="🔍 역 이름 입력" />
            </div>
            <div class="notifications">
                🔔 이벤트 12건
            </div>
            <div class="clock" id="clock">
                <!-- 시간 표시 -->
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    
    data = pd.read_csv('BigProject/Ver3_df10222.csv', encoding='utf-8')
    data['건수'] = 1
    months = []
    for i in data['일시'].values:
        months.append(int(i[5:7]))
    data['월'] = months
    #st.dataframe(data)


    col1, col2, col3 = st.columns([2.3, 5.4, 5.4])


    with col1:
        with st.container():

            st.markdown("""
           <style>
        .weather-section {
            background-color: #555555; /* 탁한 하늘색 */
            padding: 10px; /* 안쪽 여백 */
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
       
        
        </style>

        <div class="weather-section">
            <div class="weather-title">역 선택</div>
           
           
        </div>
            """, unsafe_allow_html=True)

        station = st.selectbox("", ('전체', '양원', '청량리', '가능', '가산디지털', '가산디지털구로', '가산디지털독산', '가수원', '가야',
           '가좌', '가천', '가천대', '가평', '간석', '간치', '갈매', '강릉', '강촌', '개봉', '개양',
           '개태사', '개포', '개포동', '개포예천', '거제', '건천', '경강', '경마공원', '경산', '경주',
           '경화', '계룡', '고모', '고모IEC', '고사리', '고양기지', '고잔', '고한', '공전', '과천',
           '과천청사', '과천청사과천', '관악', '관촌', '광명', '광양', '광양항', '광운대', '광운대월계',
           '광주', '광주극락강', '광주송정', '광주송정북송정', '광천', '광천청소', '괴동', '교대',
           '구례구압록', '구로', '구로차량', '구룡', '구리', '구미', '구일', '구포', '군산대야', '군산항',
           '군포', '군포금정', '극락강', '극락강동송정신호', '금릉', '금정', '금천구청', '금천구청석수',
           '금촌', '기장', '기흥', '김제', '김천', '김천구미', '김천구미칠곡IEC', '나원', '나원경주',
           '나원사방', '나전', '나주', '나한정', '남성현', '남영', '남원산성', '남창', '남창원',
           '남창월내', '남춘천', '남평', '남포', '내수', '내수오근장', '내판', '노량진', '노령',
           '노안나주', '녹양', '녹천', '논산', '능곡', '능주', '단양', '달천', '당정', '대곡', '대구',
           '대구지천', '대모산입구', '대방', '대불', '대성리', '대신', '대신아포', '대야', '대야미',
           '대전', '대전남연결', '대전조차장', '대전조차장대전', '대천', '대화', '덕소', '덕양', '덕정',
           '덕하', '도계', '도농', '도봉', '도봉산', '도심', '도안', '도원', '도원제물포', '도화',
           '독산', '동대구', '동두천', '동두천중앙', '동래', '동량', '동량목행', '동량삼탄', '동방',
           '동방경주', '동백산', '동산', '동송정신호', '동송정신호극락강', '동송정신호장', '동송정신호장극락강',
           '동암', '동인천', '동점철암', '동해', '동화', '두정', '득량', '디지털미디어시티', '마산',
           '마전', '만종', '만종원주', '망상해', '망우', '망월사', '매포', '명학', '모란', '모량',
           '모화', '모화입실', '모화호계', '목포', '목포서대전', '목행', '목행충주', '몽탄일로', '묵호',
           '묵호옥계', '묵호항', '문곡', '문단', '문산', '문수', '물금', '미금', '미평', '민둥산',
           '밀양', '반곡유교', '반성', '반월', '방학', '배방', '백마', '백산', '백석', '백양리',
           '백양사', '백운', '백운부평', '백원', '백원상주', '벌교', '벌교원창', '범계', '벽제', '병점',
           '병점차', '보성', '보정', '보천', '보천음성', '봉성봉화', '봉양', '봉양구학', '봉양제천조차장',
           '봉정', '봉화', '봉화문단', '봉화봉성', '부개', '부산', '부산기지', '부산부산진', '부산신항',
           '부산진', '부전', '부조', '부천', '부천중동', '부평', '북송정', '북영주', '분당기지', '분천',
           '불국사', '불국사입실', '비봉', '비봉의성', '사릉', '사북', '사상', '산본', '산성', '삼곡',
           '삼랑진', '삼성', '삼송', '삼척동해', '삼탄', '상록수', '상봉', '상정', '상주', '상천',
           '서광주', '서대전', '서빙고', '서생', '서울', '서울역', '서정리', '서정리평택지제', '서지',
           '서창', '서창조치원', '석불', '석수', '석포', '석포동점', '선릉', '선바위', '선평', '성균관대',
           '성환', '세류', '세천', '세천대전', '센텀', '소사', '소요산', '소요산동두천', '소이', '소정리',
           '소정리천안', '송내', '송도', '송정', '송탄', '송포', '송포임포', '수내', '수리산', '수색',
           '수서', '수서기지', '수원', '수원시청', '숙대입구', '순천', '시흥기지', '신경주', '신공덕',
           '신기', '신길', '신길온천', '신녕', '신도림', '신동', '신리', '신망리', '신성', '신이문',
           '신촌', '신탄진', '신태인', '쌍용', '아산', '아포', '아포구미', '아화건천', '안강부조',
           '안강사방', '안동', '안산', '안양', '안양군포', '안인', '안정', '안정북영주', '안평', '압록',
           '야탑', '야탑죽전', '약목', '약목왜관', '양수', '양정', '양주', '양평', '양평아신', '어등',
           '업동', '여수', '여수EXPO', '여수여천', '역곡', '연당', '연산', '연천', '연화', '영동',
           '영등포', '영등포노량진', '영등포신길', '영월', '영주', '영천', '예미', '예산', '오근장',
           '오근장내수', '오근장청주', '오류동', '오리', '오봉', '오산', '오산대', '오송', '오송공주',
           '오송청주', '오수', '오이도', '옥계', '옥계묵호', '옥곡', '옥구', '옥산', '옥천', '온수',
           '온수역곡', '온수오류동', '온양온천', '온양온천신창', '옹천', '완사', '완사진주', '왕십리', '왜관',
           '외대앞', '용문', '용산', '우보', '우암', '운길산', '운산', '운정', '울산', '울산항',
           '웅천', '원당', '원동', '원동삼랑진', '원주', '원창', '원창순천', '월계', '월내', '월롱',
           '율동경주', '율촌', '음성', '응봉', '의성', '의성비봉', '의왕', '의왕성균관대', '의정부',
           '이매', '이문', '이양', '이양능주', '이원', '이촌', '익산', '인덕원', '인천',
           '인천공항1터미널', '일광좌천', '일산', '일산백마', '임곡하남', '임기', '임포', '입석리', '입실',
           '자미원', '장성', '장항', '전곡', '전동', '전의', '전주', '점촌', '정발산', '정선', '정왕',
           '정읍', '정자', '제물포', '제천', '제천조차장', '조동', '조성', '조성벌교', '조치원', '좌천',
           '주덕', '주덕소이', '주안', '주엽', '죽동', '죽령', '죽림온천', '죽전', '중동', '중랑',
           '중리', '중앙', '증평', '지천', '지평', '지하서울', '지행', '지행덕정', '직산', '직지사',
           '진영', '진위', '진해', '창교치악', '창동', '창동기지', '창원', '창원중앙', '채운', '천안',
           '천안1지청량리', '천안소정리', '천안아산', '철암백산', '청도', '청량리', '청리', '청소',
           '청소주포', '청주', '청주오송', '청평', '청평대성리', '초남', '초성리', '초지', '추풍령',
           '춘양', '춘천', '춘포', '충주', '충주달천', '충주목행', '탄부', '탄현', '탑리', '탑리우보',
           '태평', '태화강', '통해', '퇴계원', '파주', '판대', '팔당', '평내호평', '평촌', '평촌동',
           '평택', '평택성환', '평택지제', '하남', '하남임곡', '하동', '하양', '한남', '한남서빙고',
           '한대앞', '한탄강', '한티', '함열', '함창', '함평', '행신', '현동', '호계', '호계모화',
           '호계효문', '호구포', '홍성신성', '화명', '화명구포', '화본', '화산', '화서', '화순',
           '화순능주', '화전', '화정', '황간', '황간영동', '황등', '회기', '회기청량리', '회룡', '횡성',
           '횡천', '효문', '효자', '효자괴동', '효자부조', '흑석리'))
        show_dataframe_2 = st.button(station + '역 ' + '사고 데이터')
    with col2:
        with st.container():

            # 기상 상태 섹션 스타일 정의
            st.markdown("""
           <style>
        .weather-section {
            background-color: #555555; /* 탁한 하늘색 */
            padding: 10px; /* 안쪽 여백 */
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
        </style>

        <div class="weather-section">
            <div class="weather-title">연도별 작업자사고발생수</div>
           
           
        </div>
            """, unsafe_allow_html=True)

        if station != '전체':
            data_select_2 = data[data['발생장소a']==station]
        else:
            data_select_2 = data.copy()

        data_select_2 = data_select_2.reset_index(drop=True)
        data_select_groupby_2 = data_select_2.groupby(by=['연도'], as_index = False)['건수'].sum()
        data_select_groupby_2 = data_select_groupby_2.reset_index(drop=True)

        l = len(data_select_groupby_2)
        plus = 0
        for i in range(2010, 2023):
            if i not in data_select_groupby_2['연도'].values:
                data_select_groupby_2.loc[l+plus, '연도'] = i
                data_select_groupby_2.loc[l+plus, '건수'] = 0
                plus += 1



        st.line_chart(data=data_select_groupby_2, x='연도', y='건수', width=400, height=450)

    with col3:
        
        with st.container():

            st.markdown("""
           <style>
        .weather-section {
            background-color: #555555;
            padding: 10px; /* 안쪽 여백 */
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
        </style>

        <div class="weather-section">
            <div class="weather-title">작업자사고원인별 사고발생수</div>
           
           
        </div>
            """, unsafe_allow_html=True)
        
        if station != '전체':
            data_select_3 = data[(data['발생장소a']==station)]
        else:
            data_select_3 = data.copy()

        data_select_groupby_3 = data_select_3.groupby(by=['근본원인별 상세'], as_index = False)['건수'].sum()
        fig_3 = px.pie(data_select_groupby_3, names='근본원인별 상세', values='건수', hole=.2)
        fig_3.update_traces(textposition='inside', textinfo='percent+label+value')
        fig_3.update_layout(font=dict(size=14))
        st.plotly_chart(fig_3, use_container_width=True)



    if show_dataframe_2:
            st.dataframe(data_select_2)

    left_col, main_col, right_col = st.columns([2.3, 5.4, 5.4])
    
    with left_col:
        with st.container():

            st.markdown("""
           <style>
        .weather-section {
            background-color: #555555; 
            padding: 10px; /* 안쪽 여백 */
            margin-bottom: 10px; /* 아래쪽 여백 */
        }
        .weather-title {
            font-weight: bold; /* 굵은 글씨 */
            color : #ffffff;
            font-size: 17px; /* 제목 크기 */
            margin-bottom: 8px; /* 제목 아래 여백 */
            display: block; /* 블록 레벨 요소 */
        }
        .last-col {
            margin-right: 0; /* 마지막 열은 오른쪽 여백 없음 */
        }
        </style>

        <div class="weather-section">
            <div class="weather-title" style="text-align:center">연도 선택</div>


        </div>
            """, unsafe_allow_html=True)

    with main_col:
        with st.container():
                st.markdown("""
               <style>
            .weather-section {
                background-color: #555555; 
                padding: 10px; /* 안쪽 여백 */
                margin-bottom: 5px; /* 아래쪽 여백 */

            }
            .weather-title {
                font-weight: bold; /* 굵은 글씨 */
                color : #ffffff;
                font-size: 17px; /* 제목 크기 */                
            }
            </style>
            <div class="weather-section">
                <div class="weather-title" style="text-align:center" >월별 작업자사고발생수</div>


            </div>
                """, unsafe_allow_html=True)

    with right_col:
        with st.container():   
               st.markdown("""
              <style>
           .weather-section {
               background-color: #555555; 
               padding: 10px; /* 안쪽 여백 */
               margin-bottom: 10px; /* 아래쪽 여백 */

           }
           .weather-title {
               font-weight: bold; /* 굵은 글씨 */
               color : #ffffff;
               font-size: 17px; /* 제목 크기 */                
           }
           </style>
           <div class="weather-section">
               <div class="weather-title" style="text-align:center">작업자사고원인별 사고발생수</div>


           </div>
               """, unsafe_allow_html=True)







    col4, col5, col6 = st.columns([2.3, 5.4, 5.4])

    with col4:
        year = st.selectbox('', (2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010))
        show_dataframe_5 = st.button(station + '역 ' + '사고 데이터' + '(' + str(year) + '년' + ')')
         


    with col5:
        if station != '전체':
            data_select_5 = data[(data['발생장소a']==station) * (data['연도'] == year)]
        else:
            data_select_5 = data[data['연도'] == year]

        data_select_5 = data_select_5.reset_index(drop=True)
        data_select_groupby_5 = data_select_5.groupby(by=['월'], as_index = False)['건수'].sum()
        data_select_groupby_5 = data_select_groupby_5.reset_index(drop=True)

        l = len(data_select_groupby_5)
        plus = 0
        for i in range(1, 13):
            if i not in data_select_groupby_5['월'].values:
                data_select_groupby_5.loc[l+plus, '월'] = i
                data_select_groupby_5.loc[l+plus, '건수'] = 0
                plus += 1

        st.bar_chart(data=data_select_groupby_5, x='월', y='건수', width=700, height=450)        

    with col6:
        if station != '전체':
            data_select_6 = data[(data['발생장소a']==station) * (data['연도'] == year)]

        else:
            data_select_6 = data[data['연도'] == year]
        data_select_groupby_6 = data_select_6.groupby(by=['근본원인별 상세'], as_index = False)['건수'].sum()
        fig_6 = px.pie(data_select_groupby_6, names='근본원인별 상세', values='건수', hole=.3)
        fig_6.update_traces(textposition='inside', textinfo='percent+label+value')
        fig_6.update_layout(font=dict(size=14))
        st.plotly_chart(fig_6, use_container_width=True)





    if show_dataframe_5:
        st.dataframe(data_select_5)


        
