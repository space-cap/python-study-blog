
가상 환경 만들기.


Python 가상환경을 만드는 방법은 다음과 같습니다.

### 1. `venv` 모듈을 사용하여 가상환경 생성하기 (Python 3.3 이상)

Python의 `venv` 모듈은 간단하게 가상환경을 만들 수 있게 해줍니다.

1. **터미널(또는 명령 프롬프트) 열기**

2. **가상환경 생성하기**  
   원하는 디렉토리에서 다음 명령어를 입력합니다:

   ```bash
   python -m venv 가상환경이름
   ```

   예를 들어, `myenv`라는 이름의 가상환경을 만들고 싶다면:

   ```bash
   python -m venv myenv
   ```

3. **가상환경 활성화하기**

   - **Windows**:
     ```bash
     myenv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source myenv/bin/activate
     ```

   활성화되면 터미널에 가상환경 이름이 표시됩니다. 예를 들어 `(myenv)`처럼 나타납니다.

4. **패키지 설치 등 가상환경 사용하기**  
   가상환경을 활성화한 상태에서 필요한 패키지를 설치하고 Python 코드를 실행할 수 있습니다.

5. **가상환경 비활성화하기**

   ```bash
   deactivate
   ```

이제 가상환경 설정이 완료되었습니다!