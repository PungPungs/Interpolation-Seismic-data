'''
[import programming check list]

Extenstion (3505 ~ 3506)
    1st. 3521 ~ 3528 if not 0, it's main (add. chek the tape label)
    if 3505 ~ 3506 == -1 -> trace header is variable

Clearly detect byte order (3297 - 3300)
    1. 0x01020304 (16909060) = big-endian
    2. 0x04030201 (67305985) = little-endian, etc
    3. 0x02010403 (33620995) = 16bit swap
    ---------------------------------------------
    4. 0 = this option is applies to rev 2.1 and below

Extended number of samples per data trace (3289 ~ 3292)
    1. if this data isn't 0 overrides the 3223 ~ 3224 original data

Extended sample interval of original field recording (3281 ~ 3288)
    1. if this data isn't 0 overrides the 3219 ~ 3220 original data

Extended sample interval, IEEE double precision (3273 ~ 3280)
    1. if this data isn't 0 overrides the 3217 ~ 3218 original data

Extended number of samples per data trace. (3269 ~ 3272)
    1. if this data isn't 0 ignore the 3221 ~ 3222 original data

Extended number of auxiliary traces per ensemble (3265 - 3268)
    1. if this data isn't 0 overrides the 3215 ~ 3216 original data

Extended number of data traces per ensemble
    1. if this data isn't 0 ignore the 3213 ~ 3214 original data


IF YOU NEED TO USE THIS CONFIG FILE, MAKE -1 IN THE KEY VALUE (EX. 3201, 3300 ..). PYTHON'S INDEX STARTS FROM 0.    
'''


class Seg_y_Rev2_1_Config:
    # 400-byte Binary File Header
    BINARY_FILE_HEADER = {
        3201: ("Job identification number.", 4),  # 작업 식별 번호 (예: 처리 작업 ID)
        3205: ("Line number. For 3-D poststack data, this will typically contain the in-line number.", 4),  # 라인 번호 (3D에서는 일반적으로 in-line 번호)
        3209: ("Reel number.", 4),  # 릴 번호 (과거 테이프 릴 개념, 요즘은 파일 ID처럼 사용)
        3213: ("Number of data traces per ensemble. Mandatory for prestack data.", 2),  # 하나의 앙상블(샷/위치 그룹) 당 데이터 트레이스 수 (prestack 데이터에서 필수)
        3215: ("Number of auxiliary traces per ensemble. Mandatory for prestack data.", 2),  # 하나의 앙상블 당 보조(센서/보정용) 트레이스 수
        3217: ("Sample interval. µs for time, Hz for frequency, m or ft for depth.", 2),  # 샘플 간격 (단위: µs, Hz, m, ft – 데이터 종류에 따라 다름)
        3219: ("Sample interval of original field recording.", 2),  # 원래 필드 녹음 당시 샘플 간격
        3221: ("Number of samples per data trace. (Primary data)", 2),  # 현재 데이터 트레이스당 샘플 수 (파일 내 주요 데이터 기준)
        3223: ("Number of samples per data trace for original field recording.", 2),  # 필드 녹음 당시 트레이스당 샘플 수
        3225: ("Data sample format code.", 2),  # 데이터 샘플 포맷 코드 (필수 필드)
        3227: ("Ensemble fold — The expected number of data traces per trace ensemble", 2),  # 앙상블 폴드 - 트레이스 앙상블당 예상 데이터 트레이스 수(예: CMP 폴드).
        3229: ("Trace sorting code. Type of ensemble sorting.", 2),  # 트레이스 정렬 방식 코드, 예: 1 = 기록된 그대로, 2 = CDP 앙상블, 5 = Common Source Point 등
        3231: ("Vertical sum code. N = M-1 sum, M in 2~32767.", 2),  # 수직 합산 코드 (스택 횟수 등)
        3233: ("Sweep frequency at start (Hz).", 2),  # 스윕 시작 주파수 (Hz)
        3235: ("Sweep frequency at end (Hz).", 2),  # 스윕 종료 주파수 (Hz)
        3237: ("Sweep length (ms).", 2),  # 스윕 길이 (ms)
        3239: ("Sweep type code. 1=linear, 2=parabolic, 3=exponential, 4=other", 2),# 스윕 타입 코드: 진폭 변화 방식
        3241: ("Trace number of sweep channel.", 2), # 스윕 신호를 가진 채널의 트레이스 번호
        3243: ("Sweep taper length at start (ms).", 2),  # 스윕 시작 시 테이퍼 길이 (밀리초)
        3245: ("Sweep taper length at end (ms).", 2),  # 스윕 종료 시 테이퍼 길이 (밀리초)
        3247: ("Taper type.", 2),  # 테이퍼 형태 [1=linear, 2=cos², 3=other]
        3249: ("Correlated data traces.", 2),  # 상관 처리된 데이터인지 여부. [1=no, 2=yes]
        3251: ("Binary gain recovered.", 2),  # 바이너리 게인 복구 여부 [1=yes, 2=no]
        3253: ("Amplitude recovery method.", 2),  # 진폭 복구 방법 [1=none, 2=spherical divergence, 3=AGC, 4=other]
        3255: ("Measurement system. 1=meters, 2=feet", 2),  # 측정 단위 (거리 단위). Location Data stanza와 일치해야 함
        3257: ("Impulse signal polarity.", 2), # 임펄스 극성: 압력 증가 또는 지오폰 위쪽 이동 시 신호 극성 [1=negative, 2=positive]
        3259: ("Vibratory polarity code. Signal lag angle classification", 2), # 진동 탐사 신호가 파일럿 신호보다 얼마나 지연됐는지 각도로 분류 (8단계 구간)
        3261: ("Extended number of data traces per ensemble. Overrides 3213 ~ 3214 if nonzero", 4), # 확장된 데이터 트레이스 수 (3213–3214보다 우선 적용)
        3265: ("Extended number of auxiliary traces per ensemble. Overrides 3215 ~ 3216 if nonzero", 4), # 확장된 보조 트레이스 수
        3269: ("Extended number of samples per data trace. Overrides 3221 ~ 3222 if nonzero", 4), # 확장된 트레이스당 샘플 수
        3273: ("Extended sample interval (IEEE 64-bit float). Overrides 3217~3218 if nonzero", 8), # 확장 샘플 간격 (단위 동일, 64비트 실수)
        3281: ("Extended original sample interval (IEEE 64-bit float). Overrides 3219~3220", 8), # 원본 필드 녹음 샘플 간격 (확장)
        3289: ("Extended number of samples per trace in original recording. Overrides 3223~3224", 4), # 원본 녹음에서의 트레이스당 샘플 수 (확장)
        3293: ("Extended ensemble fold. Overrides 3227~3228 if nonzero", 4), # CMP fold 확장값
        3297: ("Byte order detection constant (16909060 = 0x01020304)", 4), # 엔디안 감지용 상수. 
        3501: ("Major SEG-Y format revision number (8-bit). 0=SEG-Y 1975", 1), # SEG-Y 주요 포맷 버전
        3502: ("Minor SEG-Y format revision number (8-bit).", 1), # SEG-Y 부 버전
        3503: ("Fixed length trace flag (2-byte)", 2), # 고정된 트레이스 길이 여부 (1이면 모든 트레이스가 길이/샘플 수/간격이 동일)
        3505: ("Number of 3200-byte Extended Textual File Headers. -1=variable, 0=none", 2), # Extended Textual Header 개수. -1은 가변 길이, 0은 없음, 양수는 정확한 개수
        3507: ("Maximum number of additional 240-byte trace headers.", 2), # 추가적인 240바이트 Trace Header 블록의 최대 개수 (0이면 확장 Trace Header 없음)
        3509: ("Survey type. Sum of bit flags from 3 groups", 2),# 측선(탐사) 타입. 세 가지 그룹의 비트 플래그를 더한 값, Group 1: 환경 (1=육상, 2=해상, 3=천이대 등), Group 2: 차원 (8=1D, 16=2D, 24=3D, 32=시계열 추가) ,Group 3: 배치 (128=병렬라인, 1024=견인 스트리머 등)
        3511: ("Time basis code. 1=Local, 2=GMT, 3=Other, 4=UTC, 5=GPS", 2), # 시간 기준 코드: 로컬/UTC/GMT/GPS 등
        3513: ("Number of traces in this file or stream (64-bit unsigned).", 8), # 이 SEG-Y 파일 또는 스트림에 포함된 트레이스 수 (64비트), 0이면 Trace Header의 end-of-data 플래그 또는 EOF까지 전부가 유효
        3521: ("Offset of first trace from start of file/stream (64-bit unsigned). Overrides extended header count if nonzero.", 8), # 첫 트레이스의 바이트 오프셋 (Textual+Binary+Extended Header 포함)        # 값이 0이면 3505–3506 값을 기반으로 추정
        3529: ("Number of 3200-byte trailer stanzas after traces (4-byte signed). 0 = none, -1 = unknown", 4), # 트레일러(추가 메타데이터) 스탠자 수, -1이면 수 미정, 0이면 없음, 양수면 정확한 개수
    }


    SAMPLING_FORMAT = {
        1 : ("4-byte IBM floating-point", 4),
        2 : ("4-byte, two's complement integer", 4),
        3 : ("2-byte, two's complement integer", 2),
        4 : ("4-byte fixed-point with gain (obsolete)", 4),
        5 : ("4-byte IEEE floating-point", 4),
        6 : ("8-byte IEEE floating-point", 8),
        7 : ("3-byte two’s complement integer", 3),
        8 : ("1-byte, two's complement integer", 1),
        9 : ("8-byte, two's complement integer", 8),
        10 : ("4-byte, unsigned integer", 4),
        11 : ("2-byte, unsigned integer", 2),
        12 : ("8-byte, unsigned integer", 8),
        15 : ("3-byte, unsigned integer", 3),
        16 : ("1-byte, unsigned intege", 1),
    }

    STANDARD_TRACE_HEADER = {
        1 : ("Trace sequence number within line — Numbers continue to increase if the same line continues across multiple SEG-Y files.", 4), # trace 라인 넘버 1 ~
        5 : ("Trace sequence number within SEG-Y file — Each file starts with trace sequence one.", 4), #SEG-Y 파일 내의 추적 시퀀스 번호 - 각 파일은 추적 시퀀스 1로 시작합니다.
        9 : ("Original field record number."), # 원본 필트 레코드 번호.
        13 : ("Trace number within the original field record. "), # 원본 필드 레코드 내의 추적번호
        17 : ("Energy source point number — Used when more than one record occurs at the same effective surface location.  It is recommended that the new entry defined in Trace Header bytes 197-202 be used for shotpoint number.", 4), # ?
        25 :("Trace number within the ensemble--Each ensemble starts with trace numbers", 4), #
        29 : ("Trace identification code : ", 2), #  {-1 : Other, 0 = Unknown, 1 : Time domain seismic data, 2 : Dead, 3 : Dummy, 4 : Time break ... 16,383 : Optional}
        31 : ("Number of vertically summed traces yielding this trace.", 2), # {1 : one trace, 2 : summed traces, etc}
        33 : ("Number of horizontally stacked traces yielding this trace", 2) # {1 : one trace, 2 : two stacked traces, etc}    
        }