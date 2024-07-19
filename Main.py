from Evaluation import evaluation
import argparse
import datetime
import os
import json


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run evaluation for a model on a dataset with a given prompt.')

    parser.add_argument('--model', type=str, help='Model name')
    parser.add_argument('--dataset', type=str, help='Dataset name')
    parser.add_argument('--prompt', type=str, help='Prompt')
    args = parser.parse_args()

    for i in range(50):
        results = evaluation(args.model, args.dataset, args.prompt, Tran=False, Num=60,Sam=False)


        now = datetime.datetime.now()
        current_time = now.strftime("%H-%M-%S")
        savefile = os.path.join('D:\\Pythonfile\\MGeo-MLLMs\\Output', args.model, args.dataset + current_time+str(i) + '.json')

        with open(savefile, 'w') as json_file:
            json.dump(results, json_file)

#
#
# if __name__ == '__main__':
#     # datasets=['GEOS','Geometry3K','GeoQa+','GeoQAA+']
#     #models=[GPT4,Qwenplus,Gemin]
#     #prompts=[PAL,RaE]
#     model='GPT4'
#     datasets='Geometry3K'
#     prom='RaE'
#     results=evaluation(model,datasets,Prompt=prom,Tran=False,Num=60)
#     now = datetime.now()
#     current_time = now.strftime("%H-%M-%S")
#     savefile=os.path.join('D:\Pythonfile\MGeo-MLLMs\Output',model,datasets+current_time+'.json')
#     with open(savefile, 'w') as json_file:
#         json.dump(results, json_file)
# #[{'id': '017', 'question': 'Given Circle O with diameter CD. AB is parallel with CD and AB=80*\\degree. Find angle of arc CA.', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\GeoS\\aaai\\017.png', 'correctans': 50.0, 'length': 18, 'shape': ['circle'], 'shapenum': 1, 'total': 1, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 1, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}, {'id': '044', 'question': 'In the figure above, AD = 4, AB = 3 and CD = 9. What is the area of triangle AEC?', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\GeoS\\aaai\\044.png', 'correctans': 4.5, 'length': 21, 'shape': ['triangle'], 'shapenum': 1, 'total': 2, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 2, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}, {'id': '000', 'question': 'x + y =', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\practice\\practice\\000.png', 'correctans': 50.0, 'length': 4, 'shape': 'other', 'shapenum': 5, 'total': 3, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 3, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}, {'id': '035', 'question': 'Points A, B, C, and D are midpoints of the sides of square JETS.  If the area of JETS is 36, what is the area of ABCD?', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\GeoS\\aaai\\035.png', 'correctans': 18.0, 'length': 27, 'shape': ['square'], 'shapenum': 1, 'total': 4, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 4, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}, {'id': '026', 'question': 'Given a circle with two secants as shown at the right.  Find the measure of the arc designated by x.', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\GeoS\\aaai\\026.png', 'correctans': 25.0, 'length': 20, 'shape': ['circle'], 'shapenum': 1, 'total': 5, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 5, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}, {'id': '011', 'question': 'In the figure above, PQRS is a rectangle. The area of triangle RST is 7 and PT=2/5*PS. What is the area of PQRS?', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\official\\official\\011.png', 'correctans': 23.0, 'length': 23, 'shape': ['rectangle', 'triangle'], 'shapenum': 2, 'total': 6, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 6, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}, {'id': '063', 'question': 'In the figure above, line BE is perpendicular to line AD and line CF is perpendicular to line AD and AE = EF. What is the value of x?', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\GeoS\\aaai\\063.png', 'correctans': 60.0, 'length': 29, 'shape': ['line'], 'shapenum': 1, 'total': 7, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 7, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}, {'id': '021', 'question': 'The perimeter of the rectangle above is p and the area of the rectangle is 36. If l and w are integers, what is one possible value of p?', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\official\\official\\021.png', 'correctans': 24.0, 'length': 29, 'shape': ['rectangle'], 'shapenum': 1, 'total': 8, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 8, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}, {'id': '059', 'question': 'What is the area of the triangle below?', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\practice\\practice\\059.png', 'correctans': 4.0, 'length': 8, 'shape': ['triangle'], 'shapenum': 1, 'total': 9, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 9, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}, {'id': '027', 'question': 'In the figure above, CDE is an equilateral triangle and ABCE is a square with an area of 1. What is the perimeter of polygon ABCDE?', 'imge_path': 'D:\\Pythonfile\\MGeo-MLLMs\\Data\\GEOS\\official\\official\\027.png', 'correctans': 5.0, 'length': 26, 'shape': ['triangle', 'square'], 'shapenum': 2, 'total': 10, 'answer': 'init', 'correct': 0, 'mistake': 0, 'error': 10, 'acc ': 0.0, 'mis': 0.0, 'err': 1.0}]