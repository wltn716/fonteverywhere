import cv2
import numpy as np
import sys
import pytesseract

class getTextImages:
    def __init__(self, path):
        self.count=0
        self.path = path

    def im_trim (self,img, x1, y1, x2, y2): 
        img_trim = img[y1:y2, x1:x2]
        saved = getTextImages.get_threshold(img_trim)
        cv2.imwrite(self.path+str(self.count)+'.png',saved[1])
        return img_trim

    def get_threshold(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        return cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)


    def tesseract_rects(tesseract_boxes, img):
        rects=[]
        for line in tesseract_boxes:
            temp = line.split(" ")

            # 글자 좌표 외 원소 삭제
            temp.pop(0)
            temp.pop()

            # rectangle 그릴 때 필요한 좌표 정리
            tmp = temp[1]
            temp[1]=img.shape[0]-int(temp[3]) # 왼쪽 위 y좌표
            temp[3]=img.shape[0]-int(tmp)     # 오른쪽 아래 y좌표
            temp = [int(k) for k in temp]     # string 배열 int배열로
            rects.append(temp)

        return rects

    def contour_rects(contours):
        rects = [cv2.boundingRect(each) for each in contours]
        rects.pop(0) # 이미지 테두리 사각형 삭제
        rects = [(x,y,x+w,y+h) for (x,y,w,h) in rects]

        return rects

    def adjacent_matrix(n, rects):
        x=[0 for i in range(4)]
        y=[0 for i in range(4)]
        adj_mat = [[0]*n for i in range(n)]
        flag = 0

        for p in range(n-1):
            for q in range(p+1,n):
                if not(rects[p][0]>rects[q][2] or rects[p][2]<rects[q][0] or rects[p][1]>rects[q][3] or rects[p][3]<rects[q][1]):
                    adj_mat[p][q],adj_mat[q][p],flag=1,1,1

        return adj_mat, flag

    def get_graphs(n, adj):
        not_v = [k for k in range(n)] # 그래프에 추가되지 않은 노드
        v=[]                          # 그래프에 추가된 노드
        graphs=[]

        while len(not_v)>1:                # 그래프에 추가되지 않은 노드가 두개 이상이면 반복
            v.append(not_v[0])             # 새로운 그래프의 첫 노드
            not_v.pop(0)                   # 그래프에 추가된 노드 삭제
            for p in v:
                n2 = [k for k in not_v]
                for q in n2:
                    if adj[p][q]:                 # vertexes의 원소와 연결된 노드라면
                        v.append(q)               # vertexes에 추가
                        not_v.pop(not_v.index(q)) # not_v에서 삭제
                        
            graphs.append(v) # v 로 이루어진 하나의 그래프 생성
            v=[]             # v 집합 초기화

        if not_v: # (추가되지 않은 노드가 남았다면)단일 노드 그래프로 추가
            graphs.append(not_v)

        return graphs

    def get_combined_rects(n, adj,before):
        graphs = getTextImages.get_graphs(n, adj)
        after=[] # before은 합쳐지기 전, after는 합쳐진 후
        for graph in graphs:
            x,y=[],[]
            for index in graph:
                x.append(before[index][0])
                x.append(before[index][2])
                y.append(before[index][1])
                y.append(before[index][3])
            after.append([min(x),min(y),max(x),max(y)])

            # 사각형==노드
        adj, flag = getTextImages.adjacent_matrix(len(after),after) # 인접행렬 구하기 

        return after, adj, flag

    # @staticmethod
    def get_texts(self, img):
        img_thr = getTextImages.get_threshold(img)
        
        rects = [] # 글자 좌표 list
        
        t_boxes = pytesseract.image_to_boxes(img_thr[1], lang='kor').split('\n')
        try:
            t_boxes.pop(t_boxes.index('')) #tesseract boxes 에서 null 삭제
        except:
            pass

        if len(t_boxes)>0: # tesseract로 글자 검출 되는 경우
            rects = getTextImages.tesseract_rects(t_boxes, img)
        else:              # tesseract로 글자 검출 안되는 경우 > contour 이용
            _, contours, _ = cv2.findContours(img_thr[1], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            rects = getTextImages.contour_rects(contours)
        
        n = len(rects)                 # 사각형==노드
        adj, flag = getTextImages.adjacent_matrix(n,rects) # 인접행렬 구하기 
        while flag:
            rects, adj, flag = getTextImages.get_combined_rects(len(rects),adj,rects)


        print(rects, "최종 사각형 배열")

        for rect in rects:
            # cv2.rectangle(img, (rect[0]-1, rect[1]-1), (rect[2], rect[3]), (0, 255, 0), 1)
            getTextImages.im_trim(self,img, rect[0], rect[1], rect[2], rect[3])
            self.count+=1

        return img



# path = './imgdata/'
# new_path = './new_img/'
# if not os.path.exists(new_path):
#     os.makedirs(new_path)

# fontFile=[k for k in listdir(path) if isfile(join(path, k)) and not k[0]=='.']

# print(fontFile)

# image_files = ["./imgdata/스크린샷 2018-09-18 오후 4.42.50.PNG","./imgdata/스크린샷 2018-10-09 오전 4.56.55.PNG"]
# image_files = ["./imgdata/훈화양연화-초보-241.png","./imgdata/훈화양연화-241.png"]
# image_files = ["./imgdata/궁서체-1.png","./imgdata/궁서체-197.png"]
# image_files = ["./imgdata/test.png","./imgdata/test2.png"]

# # 이미지 읽기
# img=[]
# for file in image_files:
#     temp_i = cv2.imread(file)
#     img.append(getTextImages().get_texts(getTextImages(),temp_i))

# for i in range(len(img)):
#     cv2.imshow("img"+str(i), img[i])

# cv2.waitKey(0)
# cv2.destroyAllWindows()

