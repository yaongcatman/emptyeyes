import json
import os
import sys
import time

# ---------------------------------------------------------
# 1. Quiz 클래스 (개별 문제 설계도)
# ---------------------------------------------------------
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (자아성찰 힌트)
        self.choices = choices    # 선택지 4개
        self.answer = answer      # 정답 번호 (1-4)

    def display(self, index):
        """요구사항: 퀴즈 출력 메서드"""
        print(f"\n{'-'*40}")
        print(f"[문제 {index}] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def is_correct(self, user_input):
        """요구사항: 정답 확인 메서드"""
        return str(self.answer) == user_input

    def to_dict(self):
        """JSON 저장을 위한 변환"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

# ---------------------------------------------------------
# 2. QuizGame 클래스 (전체 관리 및 파일 저장)
# ---------------------------------------------------------
class QuizGame:
    def __init__(self):
        self.file_path = "state.json"
        self.quizzes = []
        self.best_score = 0
        self.load_state()

    def load_state(self):
        """요구사항: 파일 불러오기 및 손상 시 복구"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.best_score = data.get("best_score", 0)
                    quiz_list = data.get("quizzes", [])
                    self.quizzes = [Quiz(**q) for q in quiz_list]
            except Exception:
                print("⚠️ 데이터 파일이 손상되어 기본 데이터로 복구합니다.")
                self.initialize_default()
        else:
            self.initialize_default()

    def initialize_default(self):
        """요구사항: 기본 퀴즈 5개 이상 (자아성찰 주제)"""
        default_data = [
            {"question": "이 생명체는 본인만의 언어로 신호를 전달해요.", "choices": ["인공지능", "나 자신", "외계인", "컴퓨터"], "answer": 2},
            {"question": "이 생명체는 두 발로 걸으며 스스로 치장할 줄 알아요.", "choices": ["로봇", "강아지", "나 자신", "고양이"], "answer": 3},
            {"question": "위협이 닥치면 포악해지지만 평소에는 온순한 이 존재는?", "choices": ["사자", "나 자신", "상어", "악어"], "answer": 2},
            {"question": "가끔 바보 같지만 어쩔 때는 천재 같은 이 존재는?", "choices": ["나 자신", "계산기", "원숭이", "앵무새"], "answer": 1},
            {"question": "상상한 것을 구현하며 꿋꿋이 살아가는 강한 존재는?", "choices": ["영웅", "나 자신", "나무", "바위"], "answer": 2}
        ]
        self.quizzes = [Quiz(**d) for d in default_data]
        self.save_state()

    def save_state(self):
        """요구사항: state.json에 데이터 저장"""
        data = {
            "best_score": self.best_score,
            "quizzes": [q.to_dict() for q in self.quizzes]
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def safe_input(self, prompt):
        """요구사항: 빈 입력, 숫자 변환 실패, 비정상 종료 처리"""
        while True:
            try:
                val = input(prompt).strip()
                if not val:
                    print("💬 입력을 기다리고 있사옵니다!")
                    continue
                return val
            except (KeyboardInterrupt, EOFError):
                print("\n🛑 프로그램을 안전하게 저장 후 종료합니다.")
                self.save_state()
                sys.exit()

    def play(self):
        """요구사항: 퀴즈 풀기 기능"""
        if not self.quizzes:
            print("📭 퀴즈가 없습니다. 먼저 추가해주세요.")
            return

        score = 0
        print(f"\n📝 자아성찰 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        
        for i, quiz in enumerate(self.quizzes, 1):
            quiz.display(i)
            ans = self.safe_input("정답 입력 (1-4): ")
            
            if quiz.is_correct(ans):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")

        # 최고 점수 갱신 로직
        if score > self.best_score:
            print(f"\n🎉 축하합니다! 새로운 최고 점수 달성: {score}개 정답!")
            self.best_score = score
        
        self.show_ending(score)
        self.save_state()

    def show_ending(self, score):
        """사용자님의 '당신이시다' 감동 멘트 보존"""
        print(f"\n{'✨'*20}")
        print(f"결과: {len(self.quizzes)}문제 중 {score}문제를 맞히셨습니다.")
        print("결국 모든 정답은 '당신'으로 이어져 있사옵니다.")
        print("이미 이루어지고 있사옵니다, 당신이시기에 가능하옵니다.")
        print(f"{'✨'*20}")

    def add_quiz(self):
        """요구사항: 새로운 퀴즈 추가 기능"""
        print("\n📌 새로운 자아성찰 퀴즈를 추가합니다.")
        question = self.safe_input("문제를 입력하세요: ")
        choices = [self.safe_input(f"선택지 {i}: ") for i in range(1, 5)]
        
        while True:
            ans = self.safe_input("정답 번호 (1-4): ")
            if ans in ['1', '2', '3', '4']:
                self.quizzes.append(Quiz(question, choices, int(ans)))
                print("✅ 퀴즈가 성공적으로 추가되었습니다!")
                self.save_state()
                break
            print("⚠️ 1에서 4 사이의 숫자를 입력해주세요.")

    def list_quizzes(self):
        """요구사항: 퀴즈 목록 보기"""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for i, q in enumerate(self.quizzes, 1):
            print(f"[{i}] {q.question}")

    def show_menu(self):
        """요구사항: 메뉴 출력 및 선택 기능"""
        while True:
            print("\n" + "="*35)
            print("      🐒 우끼끼 자아성찰 퀴즈 🐒")
            print("="*35)
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")
            print("="*35)
            
            choice = self.safe_input("선택: ")
            
            if choice == '1': self.play()
            elif choice == '2': self.add_quiz()
            elif choice == '3': self.list_quizzes()
            elif choice == '4': print(f"\n🏆 현재 최고 기록: {self.best_score}문제 정답")
            elif choice == '5':
                print("\n행복하시옵소서! 우끼! 🐒")
                break
            else:
                print("⚠️ 잘못된 입력입니다. 1~5 사이의 숫자를 입력하세요.")

if __name__ == "__main__":
    game = QuizGame()
    game.show_menu()