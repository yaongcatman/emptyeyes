import json
import os
import sys
import time

# ---------------------------------------------------------
# 1. Quiz 클래스 (개별 퀴즈 정보)
# ---------------------------------------------------------
class Quiz:
    def __init__(self, answer_word, hints, themes):
        self.answer_word = answer_word
        self.hints = hints    # 10개의 힌트 리스트
        self.themes = themes  # 10개의 테마 이름 리스트

    def display_hint(self, index):
        print(f"\n============================================================")
        print(f"🐒 [제 {index + 1}단계 특징: {self.themes[index]}]")
        print(f"📢 {self.hints[index]}")
        print(f"============================================================")

    def is_correct(self, user_input):
        clean_input = user_input.strip()
        # "나", "저" 등 본인을 지칭하는 정답 인정
        return clean_input in [self.answer_word, "나", "저", "나 자신", "me", "당신"]

    def to_dict(self):
        return {
            "answer_word": self.answer_word,
            "hints": self.hints,
            "themes": self.themes
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
        """데이터 로드 및 파일이 없으면 기본 퀴즈 생성"""
        default_hints = [
            "이 생명체는 본인만의 언어를 가지고 신호를 전달할 수 있어요.",
            "이 생명체는 두 발로 걸을 수 있어요.",
            "밥을 주지 않거나 위협이 닥치면 포악해지지만 평소에는 온순해요.",
            "이 생명체는 스스로 치장할 줄 알아요.",
            "척박한 환경 속에서도 스스로 살아남는 방법을 터득해요.",
            "이 생명체는 방구도 낄 줄 알아요.",
            "눈에 보이고 들리는 것을 스스로 학습할 줄 알아요.",
            "가끔 바보같지만 어쩔 때는 천재같아요.",
            "본인이 상상한 것을 구현할 줄 알아요.",
            "본인을 포기하지 않고 꿋꿋이 살아가는 강한 생명체예요."
        ]
        default_themes = [
            "말하는 원숭이", "걷는 원숭이", "포악한 원숭이", "치장하는 원숭이",
            "생존왕 원숭이", "방구 뀌는 원숭이", "공부하는 원숭이", "천재 원숭이",
            "상상하는 원숭이", "포기하지 않는 원숭이"
        ]

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.best_score = data.get("best_score", 0)
                    # 리스트가 비어있지 않은지 확인
                    quiz_data = data.get("quizzes", [])
                    if quiz_data:
                        self.quizzes = [Quiz(**q) for q in quiz_data]
                    else:
                        self.initialize_default(default_hints, default_themes)
            except Exception:
                print("⚠️ 데이터 손상! 기본 데이터로 복구합니다.")
                self.initialize_default(default_hints, default_themes)
        else:
            self.initialize_default(default_hints, default_themes)

    def initialize_default(self, hints, themes):
        """초기 퀴즈 설정"""
        self.quizzes = [Quiz("나", hints, themes)]
        self.save_state()

    def save_state(self):
        """JSON 파일로 저장"""
        data = {
            "best_score": self.best_score,
            "quizzes": [q.to_dict() for q in self.quizzes]
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def slow_print(self, text, speed=0.05):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(speed)
        print()

    def safe_input(self, prompt):
        while True:
            try:
                val = input(prompt).strip()
                # 빈 입력 방지 (과제 요구사항)
                if not val:
                    print("💬 우끼! 아무것도 입력하지 않으면 진행할 수 없사옵니다!")
                    continue
                return val
            except (KeyboardInterrupt, EOFError):
                print("\n\n🛑 비정상 종료 감지! 안전하게 저장 후 종료합니다.")
                self.save_state()
                sys.exit()

    def play(self):
        if not self.quizzes:
            print("📭 퀴즈 데이터가 없습니다.")
            return

        quiz = self.quizzes[0]
        success = False
        print("\n" + "🐒" * 25)
        print("   우끼끼! 터미널 열고개 퀴즈")
        print("🐒" * 25)

        for i in range(10):
            quiz.display_hint(i)
            ans = self.safe_input("🤔 정답 입력: ")

            if quiz.is_correct(ans):
                print("\n🎊🎊🎊 허거덩스바리 ~ 정답입니다 ~ 🎊🎊🎊")
                success = True
                self.best_score = 100 # 최고 점수 갱신
                break
            else:
                print("\n에잉! 쯧! 틀릴 때마다 응원의 뽀뽀! 쪽! 😘")

        self.show_ending(success)
        self.save_state()

    def show_ending(self, success):
        print("\n" + "✨" * 40)
        if not success:
            print("(정답은 당신이었습니다. 엔터를 눌러 축복을 받으세요...)")
            input()
        
        self.slow_print("이 모든 것을 할 줄 아는 생명체는 바로 당신! 바로 너!")
        self.slow_print("당신이시다, 오직 당신이시다, 중심에 서 계신 분은 오직 당신이시다.")
        
        ment = [
            "숨 한 번에 공기가 고개를 숙이고, 발걸음 하나에 길이 먼저 펼쳐진다",
            "다 잘될 것이옵니다, 이미 흐르고 있사옵니다, 거스를 수 없사옵니다",
            "넘어지셔도 괜찮사옵니다, 대지가 받들어 다시 올려드릴 것이옵니다",
            "이미 이루어지고 있사옵니다, 지금 이 순간도 완성으로 향하고 있사옵니다",
            "그러니 나아가시옵소서, 당신이시기에 반드시 이루어질 것이옵니다. 🐒💎"
        ]
        for line in ment:
            time.sleep(0.5)
            self.slow_print(line, 0.04)
        print("✨" * 40)

    def show_menu(self):
        while True:
            print("\n" + "="*20)
            print("🍌 우끼끼 퀴즈 메뉴")
            print("="*20)
            print("1. 바로 퀴즈 시작")
            print("2. 최고 점수 확인")
            print("3. 종료")
            
            choice = self.safe_input("메뉴 선택: ")
            
            if choice == '1':
                self.play()
            elif choice == '2':
                print(f"\n🏆 현재 최고 기록: {self.best_score}점")
            elif choice == '3':
                print("\n행복하시옵소서! 우끼! 🐒")
                break
            else:
                print("\n❌ 잘못된 입력입니다. 1, 2, 3 중에서 골라주세요.")

if __name__ == "__main__":
    game = QuizGame()
    game.show_menu()
    