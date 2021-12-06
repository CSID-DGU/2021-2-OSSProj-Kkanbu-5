# 2021-2-OSSProj-KKANBU-5
-------------
[![GitHub license](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/CSID-DGU/2021-2-OSSProj-Kkanbu-5/blob/main/LICENSE)
[![OS](https://img.shields.io/badge/OS-ubuntu-red)](https://ubuntu.com)
[![Python version](https://img.shields.io/badge/python-3.5.2-brightgreen.svg)](https://www.python.org)
[![Pygame version](https://img.shields.io/badge/pygame-2.0.0-yellow.svg)](http://pygame.org)  
**Team Leader**: [[심미경](https://github.com/Sim-mi-gyeong)]   
**Team Member**: [[김성호](https://github.com/sungho17)], [[조수빈](https://github.com/jo-soobin)]

## How to play
### Installation (OS: Ubuntu)
1. 터미널에 `git clone https://github.com/CSID-DGU/2021-2-OSSProj-Kkanbu-5.git ` 입력  

2. `pip3 install pygame` 입력  

3. `pip3 install pymysql` , `pip3 install bcrypt` 입력  

3. `cd Kkanburis` 입력  

4. `python3 Kkanburis_ver2.py` 입력   

### 조작키 안내
<img src="Kkanburis/assets/vector/help_contents.png" width="500" height="250"> 

## Introduce
### Base Source
2020-1 Openmind [OMPYTRIS](https://github.com/CSID-DGU/2020-1-OSSP1-OpenMind-1)

#### <모드>
- Single mode 
- PvP mode
  
## 새로운 기능

### 1. 회원가입 및 로그인  
게임 시작 첫화면인 회원가입 및 로그인 선택 페이지    
  
<img src="PBSPYTRIS/assets/Screenshots/login1.png" width="500" height="250">   
  
singup 클릭시 회원가입을 할 수 있는 페이지   
  
<img src="PBSPYTRIS/assets/Screenshots/signup.png" width="500" height="250">  
  
 signup 완료시 로그인을 할 수 있는 페이지  
    
<img src="PBSPYTRIS/assets/Screenshots/signin.png" width="500" height="250">  


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
* -배경 이미지: (http://www.freepik.com)  
* -보드 이미지: (https://github.com/CSID-DGU/2020-1-OSSP1-OpenMind-1/tree/master/OMPYTRIS/assets/vector)
* -버튼 이미지: (https://www.miricanvas.com/)
* -로그인 페이지 이미지: (https://github.com/CSID-DGU/2021-1-OSSPC-BINSU-7)  

## References
* (https://github.com/CSID-DGU/2020-1-OSSP1-OpenMind-1)  
* (https://github.com/CSID-DGU/2021-1-OSSPC-BINSU-7)  