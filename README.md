# 2021-2-OSSProj-KKANBU-5
-------------
[![GitHub license](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/CSID-DGU/2021-2-OSSProj-Kkanbu-5/blob/main/LICENSE)
[![OS](https://img.shields.io/badge/OS-ubuntu-red)](https://ubuntu.com)
[![Python version](https://img.shields.io/badge/python-3.5.2-brightgreen.svg)](https://www.python.org)
[![Pygame version](https://img.shields.io/badge/pygame-2.0.0-yellow.svg)](http://pygame.org)  
**Team Leader**: [심미경(https://github.com/Sim-mi-gyeong)]   
**Team Member**: [김성호(https://github.com/sungho17)]
                 [조수빈(https://github.com/jo-soobin)]

## How to play
### Installation (OS: Ubuntu)
1. `git clone https://github.com/CSID-DGU/2021-2-OSSProj-Kkanbu-5.git ` 

2. `pip3 install pygame` 

3. `pip3 install pymysql` 
   `pip3 install bcrypt` 

3. `cd Kkanburis` 

4. `python3 Kkanburis_ver2.py` 

### Main Page
<img src="Kkanburis/assets/vector/main_page.JPG" width="500" height="250"> 

### 조작키 안내
<img src="Kkanburis/assets/vector/help_contents.png" width="500" height="250"> 

## Introduce
### Base Source
2020-1 Openmind [OMPYTRIS](https://github.com/CSID-DGU/2020-1-OSSP1-OpenMind-1)

#### <모드>
- Single mode: 한 명의 Player가 단독으로 게임 플레이. 콤보 아이템, 방해 블록 기능
- PvP mode: 두 명의 Player가 각각의 키보드 사용. 콤보 발생으로 상대방 ATTACK 기능. 게임 종료 후 승자의 점수 저장
  
## 새로운 기능

### 1. 회원가입 및 로그인  
 -OMPYTRIS: Leadearboard.txt 파일로 점수를 저장하고 리더보드에 나타나는 방식   
 -KKANBURIS: 로그인 정보를 AWS에 연동하여 전역적인 점수 저장 및 확인 가능

게임 실행 시 첫 화면(sign in, sign up, quit)

<img src="Kkanburis/assets/vector/login_main.JPG" width="500" height="250">   

sign in 클릭 시

<img src="Kkanburis/assets/vector/signin_page.JPG" width="500" height="250">

singup 클릭시
  
<img src="Kkanburis/assets/vector/singup_page.JPG" width="500" height="250">  



## Score board
| Action             | Score                              |
|--------------------|------------------------------------|
| Block drop         | 10 * level                         |
| Erase 1 line       | 50 * level * 1 + combo_count       |
| Erase 2 lines      | 150 * level * 2 + 2 * combo_count  |
| Erase 3 lines      | 350 * level * 3 + 3 * combo_count  |
| Erase 4 lines      | 1000 * level * 4 + 4 * combo_count |
| Erase Rainbow line | 500 * rainbow_count                |


## Credits
* 배경 이미지: (http://www.freepik.com)  
* 보드 이미지: (https://github.com/CSID-DGU/2020-1-OSSP1-OpenMind-1/tree/master/OMPYTRIS/assets/vector)
* 버튼 이미지: (https://www.miricanvas.com/)
* 로그인 페이지 이미지: (https://github.com/CSID-DGU/2021-1-OSSPC-BINSU-7)  

## References
* Base Source: (https://github.com/CSID-DGU/2020-1-OSSP1-OpenMind-1)  
* Login Page: (https://github.com/CSID-DGU/2021-1-OSSPC-BINSU-7)  