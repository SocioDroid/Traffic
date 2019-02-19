
import os
import sys
video_name = str(sys.argv[1])
os.environ['OPENALPR_LICENSE_KEY'] = "SEpKS0xNTk3z7uHq6+H06OHtuLu9tNHo/fD7/6Wgo6auqqipqq6vqpWQlJCWl5CUAhDzrF0KSjxwQrooqklk8rSZ+jARzHYQWspB08/ohWmu2SU5Y/xAA60xxrM7TJLaOH0GworV8SOqyaVgLnLpXGzYnUkEfGNqf7b3Vol9q7dvezCvZ2dJ9n3q4RyN6FQv "
os.system('alpr -c in '+video_name+' >> out.txt')
os.system('python get_plate_no.py out.txt '+video_name)