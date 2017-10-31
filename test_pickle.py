import pickle
import teachinbot

bot = teachinbot.Teachinbot()
print(bot.get_all_lecturers())
b_data = pickle.dumps(bot.get_all_lecturers())
data = pickle.loads(b_data)
print(data[0])

# bot.add_lecturer(1234)
# print(bot.get_all_lecturers())