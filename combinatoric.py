import numpy as np

class Combinatoric:
    def __init__(self):
        pass

    
    '''Вычислить число сочетаний без повторений'''
    def combinations_without_repeats(n, m):
        arr = [m, n-m]     # определить основания факториалов в знаменателе
        maximum = max(arr) # определить максимум из оснований факториалов знаменателя
        minimum = min(arr) # определить минимум из оснований факториалов знаменателя

        # Определить число сочетаний. В числителе n!, сокращенный на факториал максимума, в знаменателе факториал минимума 
        result = np.prod(np.arange(maximum + 1, n + 1, 1, dtype=np.object)) // np.math.factorial(minimum)     
        return result


    '''Вычислить число сочетаний с повторениями'''
    def combinations_with_repeats(n, m):
        n = n + m - 1                                            # переопределить n для перехода к формуле сочетаний
        result = Combinatoric.combinations_without_repeats(n, m) # определить число сочетаний для нового значения n
        return result


    '''Вычислить число размещений с повторениями'''
    def accommodation_with_repeats(n, m):
        return n**m

