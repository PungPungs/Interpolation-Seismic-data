# Cpp를 이용한 segy 프로그램 제작 프로젝트

#### 6/3 배운 점
1. opertaor new : 메모리 할당 함수 + 생성자
    ----
    - 가변 구조체의 크기를 선언시에 할당하기 위한 방법이다. binary파일에서 데이터의 길이를 알아야하기 때문에 값을 구하고 메모리 공간을 확보하면서 생성하기 위한 함수이다.
    - typedef sturct 같은 데이터타입만 선언되어 있는 객체에 이런 방식으로 사용 가능하다고 한다.


    ```cpp
    SegyTrace* trace = operator new(total_size); // 메모리 할당
    operator delete (trace); // 메모리 해제
    ```
2. static_cast : 컴파일 타임에서 결정되는 타입 변경 함수
    ----
    - 의미 있는 변환에서 사용할 수 있는 함수이다. 즉 5는 5.0도 될 수 있다 그래서 변경이 허용된다. 하지만 5의 경우 문자열로 바꾸라고 하면 이거는 바꿀 수 없다.(근데 "5" 로 바꾸면 안 되나??) 라고 의문을 가졌으나... <> 안에 들어가는 타입이 바꿀 수 있는 생성자를 가져야한다고 한다.
    ```cpp
    int x = 5;
    float y = static_cast<float>(x);
    ```
#### 느낀 점
- 파이썬에 비해 너무 복잡하고 머리 아프다.. 하지만 익숙해지면 정말 재밌을 거 같다.


#### 6/4 코드 작성 중 문제 상황
------
1. 트레이스의 길이는 바이너리에서 데이터를 읽어온 후 판별해야하는 문제가 있어 가변적이다. 개발하는 나의 입장에서 보기 편하기 위해 연속적이진 않지만 배열로 할당을 했는데 구조체 선언시 고정 상수가 컴파일 타임에 할당되어야 한다고 한다. 더블 포인터를 쓰면 된다고 하지만 아직 미숙하고 유지보수하기에는 어려울 거 같아 전체 메모리 읽은 후 함수를 선언하여서 접근하는 방식으로 이용하여야겠다..

##### 문제 상황
```cpp
    int trace_length = (static_cast<int>(size.QuadPart) - 3600) / ((dt*4) + 240);
    SegyTrace* trace[trace_length] ;
    size_t len = sizeof(SegyTrace) + (sizeof(float) * dt);
    for (int i = 0; i < 13484; i++) {
        trace[i] = (SegyTrace*)operator new(len);
        DWORD bytesRead;
        bool success_2 = ReadFile(hfile, trace[i], (DWORD)len, &bytesRead, NULL);
        if (success_2 == TRUE) {
            trace_start = trace_start + (LONG)len;
            SetFilePointer(hfile, trace_start, NULL, FILE_BEGIN);;
        }
    }
```
##### 해결 상황