# Interpolation-Seismic-data
Korean : 이 프로젝트는 머신러닝 시스템을 이용하여 sgy를 보간하기 위한 프로젝트 입니다. 아마 아주 긴 프로젝트가 될 것 입니다. 왜냐하면 저를 위한 seg-y 프로그램을 계획 중이기 떄문 입니다.
English : This project uses a ML system to interpolation seismic data. Maybe It's a very long project. Beacuse I'll also planning to create seg-y program just for me

# CHATER 1
 - Korean : 저는 컴퓨터 공학을 전공했습니다. 하지만 저는 seg-y 프로그램을 만들고 싶습니다. 왜냐하면 우리 회사는 해양 탐사 기업이며 우리는 많은 seg-y 파일이 있기 때문입니다. 나의 최종 목표는 sgy 데이터 보간하여 직원들의 시간을 절약하는 것 입니다.
 - English : I majored computer engineering but i want to create seg-y program. because our company is  ocean exploration company and we have a lot of segy file. My ultimate goal is to save  my company staff  time by interpolating seismic data

 - Korean : 먼저 seg-y 설정 파일을 만들고 최적화를 시킬 것 입니다. 낮은 레벨의 프로그래밍 언어를 쓰고 싶으나 하기에는 기술이 뛰어나지 않습니다. 그래서 제 생각은 이 프로젝트가 끝나고 충분한 시간이 있으면 최적화를 할 생각 입니다. 
 - English : First, I will create a seg-y configuration file and then proceed with optimization. I want to use a low-level programming language, but I don't have the skills to do so. So I'm thinking of giving it a try once I'm done with this project and have enough time to optimize it.

# Python
 - Korean : 먼저 ver3까지 구성하였습니다. 버전 1은 단순히 라이브러리의 개념이 아닌 해석하고자 하는데 목표를 두었고 버전 2는 조금 각 기능을 분리하려고 하였으나 전반적인 프레임이 짜여지지 않아 실패하였습니다. 버전 3는 어느 정도 프레임을 갖췄으나 제가 원하는 속도가 나오지 않았고 너무 복잡하였습니다. 또한 csv 파일로 변환시 너무나 많은 시간이 걸려 최적화를 고민 중이었습니다.
 - 버전별 코드 작성 이유 설명 필요()

# C
 ### 정리
 - 얼마전 구조체를 사용시 바이너리 파일을 읽으면 정해진 구조체의 속성 및 길이에 따라 파싱된다는 사실을 발견했습니다. 코드를 비약적으로 줄일 수 있고 제가 원하는 깔끔함, 속도까지 줄일 수 있게 되었습니다. 아마 파이썬은 추후 머신러닝을 위한 도구로만 사용될 거 같습니다. 
 
 ---
 ### C를 프로그래밍 하면서 배운 점 및 의문점
 1. 배운점
    - 메인부 혹은 함수에서 변수를 선언하면 그 모든 변수는 스택이라는 영역에 할당된다. 스택은 접근과 처리가 빠르지만 공간이 많지 않아 효율적으로 사용해주어야 한다. 엔드엔트리 혹은 함수 종료시 자동으로 메모리를 해제한다.
    - 힙은 malloc, free 라는 함수로 메모리를 할당, 해제할 수 있다. 보통 큰 데이터 및 함수 종료시에도 사라지만 안 되는 데이터를 위해 사용되는 공간이다. 스택보다 느리지만 사용 가능한 공간은 더 많아서 효율적으로 사용할 수록 좋다.

2. 의문점
    - 수 많은 개발자들이 C의 메모리 누수로 인하여 해킹을 당하고 프로그램의 치명적인 버그가 생긴다고 하였다. 그러면 동적 메모리 할당시 딕셔너리 형태로 (Ex. "kill" : True) 메모리 할당 여부를 기록하고 프로그램 종료시 만약 FALSE 인 변수를 찾아 헤제하면 되지 않을까 하는 의문이 든다. 분명 누군가는 생각했을 부분이고 시도도 해본 부분이겠지만 찾아봐야겠다.