import os
import pickle
from collections import defaultdict

# 시간표의 기본 정보를 저장할 클래스
class TimeTable:
    """
        시간표 테이블에서 필요한 정보를 클래스 변수로 정의
    """
    # 테이블 제목
    title = 'TimeTable'
    # 테이블 구분선
    divider = "-" * 13
    # 테이블 헤더
    table_head = ["", " ", "M", "T", "W", "T", "F", ""]
    # 사용자가 요일을 입력했을 때, 월 ~ 금에 해당하는 값을 미리 정의
    weeks = { "월": 2, "화": 3, "수": 4, "목": 5, "금": 6 }
    # 등록된 시간표의 정보를 저장할 딕셔너리
    """
    예시)
    {
        "class_name": [ # 수업 알파벳
        { 
            "day": ~, # 수업 요일 (문자 형식 ex) 월, 화, 수, 목)
            "start_time": ~, # 수업 시작 시간
            "end_time": ~ # 수업 끝 시간
        },
        ...
      ]
      ...
    }
    """
    histories = defaultdict(list)
    # txt 파일명
    txt_file = "timetable.txt"
    # pickle 파일명
    pickle_file = "timetable.pkl"

    # 초기 테이블 바디
    table_body = [
        ["", "1", " ", " ", " ", " ", " ", ""],
        ["", "2", " ", " ", " ", " ", " ", ""],
        ["", "3", " ", " ", " ", " ", " ", ""],
        ["", "4", " ", " ", " ", " ", " ", ""],
        ["", "5", " ", " ", " ", " ", " ", ""],
        ["", "6", " ", " ", " ", " ", " ", ""],
        ["", "7", " ", " ", " ", " ", " ", ""],
        ["", "8", " ", " ", " ", " ", " ", ""],
    ]

    # 테이블을 출력해주는 메소드
    def print_table(self):
        print(f'[ {TimeTable.title} ]')
        print(TimeTable.divider)
        print("|".join(TimeTable.table_head))
        print(TimeTable.divider)
        for row in TimeTable.table_body:
            print("|".join(row))
        print(TimeTable.divider)

    # 파일에 시간표 정보를 쓰는 메소드
    def wirte_file_table(self, file):
        file.write(f'[ {TimeTable.title} ]\n')
        file.write(f'{TimeTable.divider}\n')
        file.write(f'{"|".join(TimeTable.table_head)}\n')
        file.write(f'{TimeTable.divider}\n')
        for row in TimeTable.table_body:
            file.write(f'{"|".join(row)}\n')
        file.write(f'{TimeTable.divider}\n')

    # 수업을 등록시키는 메소드
    def register_class(self, table_info):
        # 시간표를 계속 등록하기를 원하면 등록하려는 수업 정보를 입력 받음
        day, start_time, end_time, target_day, day, class_name = table_info
        # 수업 시간이 0교시나 8교시를 초과하는 즉, 1교시 ~ 8교시가 아니라면
        if start_time < 1 or end_time > 8:
            # 에러 메시지 출력 후 continue
            print(">>> [ERROR] 등록하려는 수업이 등록 가능 시간을 벗어납니다!")
            return

        # 수업 시작 시간부터 끝시간까지 수업 알파벳을 채워넣기 위해 순회
        for row in range(start_time - 1, end_time):
            # 만약 해당 시간에 수업이 있으면 에러 메시지 출력 후 for문 종료
            if TimeTable.table_body[row][target_day] != " ":
                print(">>> [ERROR] 해당 시간에 이미 수업이 있습니다!")
                return
    
            # 수업을 등록할 수 있으면 해당 시간에 수업 등록
            TimeTable.table_body[row][target_day] = class_name

        TimeTable.histories[class_name].append({ "day": day, "start_time": start_time, "end_time": end_time })

    # 수업을 삭제하는 메소드
    def delete_class(self, delete_class_name):
        if not delete_class_name in TimeTable.histories:
            print(f'{delete_class_name} 수업은 등록되어 있지 않습니다.')
            return

        for history in TimeTable.histories[delete_class_name]:
            day, start_time, end_time = history["day"], history["start_time"], history["end_time"]
            target_day = TimeTable.weeks[day]
            # 수업을 삭제하기 위해 순회
            for row in range(start_time - 1, end_time):  
                # 수업 삭제
                TimeTable.table_body[row][target_day] = " "

        # histories에서 해당 수업 삭제
        del TimeTable.histories[delete_class_name]

    # 시간표를 txt 파일로 저장하는 메소드
    def save_timetable_to_txt(self):
        # 텍스트로 저장하는 경우
        try:
            with open(TimeTable.txt_file, "w") as file:
                self.wirte_file_table(file)
                print(f'>>> {TimeTable.txt_file} 파일이 저장되었습니다!')
        except Exception as error:
            print("===============================")
            print(error)
            print("===============================")

    # 시간표를 pkl 파일로 저장하는 메소드
    def save_timetable_to_pickle(self):
        # 딕셔너리로 저장하는 경우
        try:
            with open(TimeTable.pickle_file, "wb") as file:
                pickle.dump(TimeTable.histories, file)
                print(f'>>> {TimeTable.pickle_file} 파일이 저장되었습니다!')
        except Exception as error:
            print("===============================")
            print(error)
            print("===============================")

    # txt 파일로부터 시간표를 불러오는 메소드
    def read_timetable_from_txt(self):
        exists = os.path.isfile(TimeTable.txt_file)
        if exists:
            with open(TimeTable.txt_file, "r") as file:
                print(">>> 불러온 시간표입니다. <<<")
                for line in file.readlines():
                    print(line, end="")
        else:
            print(">>> 불러올 시간표가 없습니다.")

    # pickle 파일로부터 시간표를 불러오는 메소드
    def read_timetable_from_pickle(self):
        exists = os.path.isfile(TimeTable.pickle_file)
        if exists:
            with open(TimeTable.pickle_file, "rb") as file:
                histories = pickle.load(file)
                # 수업 시작 시간부터 끝시간까지 수업 알파벳을 채워넣기 위해 순회
                for class_name, info_list in histories.items():
                    for info in info_list:
                        target_day = TimeTable.weeks[info["day"]]
                        for row in range(info["start_time"] - 1, info["end_time"]):
                            # 해당 시간에 수업 등록
                            TimeTable.table_body[row][target_day] = class_name

                print(">>> 불러온 시간표입니다. <<<")
                self.print_table()
        else:
            print(">>> 불러올 시간표가 없습니다.")

# 질문을 저장할 클래스
class Question:
    def __init__(
        self,
        print_error,
        register_class,
        delete_class,
        save_timetable_to_txt,
        save_timetable_to_pickle,
        read_timetable_from_txt,
        read_timetable_from_pickle
    ):
        self.print_error = print_error
        self.register_class = register_class
        self.delete_class = delete_class
        self.save_timetable_to_txt = save_timetable_to_txt
        self.save_timetable_to_pickle = save_timetable_to_pickle
        self.read_timetable_from_txt = read_timetable_from_txt
        self.read_timetable_from_pickle = read_timetable_from_pickle

    # 시간표를 등록할지, 삭제할지 물어보는 메소드
    def register_or_delete_question(self):
        print(">>> 1: 시간표 등록 <<<")
        print(">>> 2: 시간표 삭제 <<<")
        action = input(">>> 원하시는 메뉴를 눌러주세요 : ")

        # 입력된 값이 유효한지 확인하는 변수
        is_valid = action.isdigit() and (int(action) == 1 or int(action) == 2)
        # 입력된 값이 유효하지 않다면
        if not is_valid:
            self.print_error(action)
            # 재귀 호출
            self.register_or_delete_question()
    
        action = int(action)
        # 수업을 등록하는 경우
        if action == 1: self.register_class_question()
        # 수업을 삭제하는 경우
        elif action == 2: self.delete_class_question()

    # 등록하려는 수업 정보를 입력 받는 메소드
    def register_class_question(self):
        [day, period] = input(">>> 등록할 수업의 요일과 교시를 입력하세요: ").split(" ")
        time = int(input(">>> 등록할 수업의 연강 시간을 입력하세요: "))
        class_name = input(">>> 등록할 수업의 알파벳을 입력하세요: ")

        # 등록하려는 요일
        target_day = TimeTable.weeks[day]
        # 수업 시작 시간
        start_time = int(period)
        # 수업 끝 시간
        end_time = start_time + time - 1
        self.register_class([ day, start_time, end_time, target_day, day, class_name ])

    # 삭제하려는 수업 정보를 입력받는 메소드
    def delete_class_question(self):
        class_name = input(">>> 삭제할 수업의 알파벳을 입력하세요: ")
        self.delete_class(class_name)

    # 시간표를 저장할지 불러올지 물어보는 메소드
    def save_or_read_question(self):  
        print(">>> 1: 시간표 저장 <<<")
        print(">>> 2: 시간표 불러오기 <<<")
        action = input(">>> 원하시는 메뉴를 눌러주세요 : ")

        # 입력된 값이 유효한지 확인하는 변수
        is_valid = action.isdigit() and (int(action) == 1 or int(action) == 2)
        # 입력된 값이 유효하지 않다면
        if not is_valid:
            self.print_error(action)
            # 재귀 호출
            self.save_or_read_question()

        action = int(action)
        # action 값에 따라 시간표 저장 또는 불러오는 함수 호출
        if action == 1: self.save_question()
        elif action == 2: self.read_question()

    # 시간표 저장 방법을 묻는 메소드
    def save_question(self):
        print(">>> 1: txt 파일로 저장")
        print(">>> 2: pkl 파일로 저장")
        print(">>> 3: 둘 다 저장")
        action = input(">>> 원하시는 메뉴를 눌러주세요 : ")

        # 입력된 값이 유효한지 확인하는 변수
        is_valid = action.isdigit() and (int(action) == 1 or int(action) == 2 or int(action) == 3)
        # 입력된 값이 유효하지 않다면
        if not is_valid:
            self.print_error(action)
            # 재귀 호출
            self.save_question()

        action = int(action)
        # txt 파일로 저장하는 경우
        if action == 1:
            self.save_timetable_to_txt()
        # pkl 파일로 저장하는 경우
        elif action == 2:
            self.save_timetable_to_pickle()
        # 둘 다 저장하는 경우
        elif action == 3:
            self.save_timetable_to_txt()
            self.save_timetable_to_pickle()

    # 저장된 시간표를 불러오는 메소드
    def read_question(self):
        print(">>> 1: 텍스트")
        print(">>> 2: 딕셔너리 ")
        action = input(">>> 불러올 파일을 선택하세요 : ")

        # 입력된 값이 유효한지 확인하는 함수
        is_valid = action.isdigit() and (int(action) == 1 or int(action) == 2)
        # 입력된 값이 유효하지 않다면
        if not is_valid:
            self.print_error(action)
            # 재귀 호출
            self.read_question()

        action = int(action)
        # txt 파일을 불러오는 경우
        if action == 1: self.read_timetable_from_txt()
        # pkl 파일을 불러오는 경우
        elif action == 2: self.read_timetable_from_pickle()

# 에러 로그를 저장하는 클래스
class Error:  
    # 입력값이 잘못되었을때, 출력해주는 메소드
    def print_error(self, input):
        print(f'잘못된 입력값입니다. => ({input})')

class Main:
    def run(self):
        timetable = TimeTable()
        error = Error()
        question = Question(
            error.print_error,
            timetable.register_class,
            timetable.delete_class,
            timetable.save_timetable_to_txt,
            timetable.save_timetable_to_pickle,
            timetable.read_timetable_from_txt,
            timetable.read_timetable_from_pickle
        )
    
        print(">>> 현재 시간표입니다. <<<")
        timetable.print_table()
        print(">>> 1: 시간표 편집 <<<")
        print(">>> 2: 시간표 저장 또는 불러오기 <<<")
        print(">>> 3: 시간표 프로그램 종료 <<<")
        action = input(">>> 원하시는 메뉴를 눌러주세요 : ")
        # 입력된 값이 유효한지 확인하는 함수
        is_valid = action.isdigit() and (int(action) == 1 or int(action) == 2 or int(action) == 3)
        # 입력된 값이 유효하지 않다면
        if not is_valid:
            print("잘못된 입력입니다.")
            # 재귀 호출
            self.run()
      
        action = int(action)
        if action == 3:
            print(">>> 시간표 프로그램이 종료되었습니다. <<<")
            return
    
        if action == 1:
            question.register_or_delete_question()
        elif action == 2:
            print(">>> 최종 시간표입니다. <<<")
            timetable.print_table()
            question.save_or_read_question()
  
        self.run()
  

 # 시간표 프로그램 시작
main = Main()
main.run()
