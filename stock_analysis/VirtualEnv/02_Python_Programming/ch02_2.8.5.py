import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# pip install --upgrade setuptools wheel
# pip install matplotlib==3.7.5
# 2.8.5 맷플롯립으로 이미지 가공하기
plt.suptitle('Image Processing', fontsize=18)
plt.subplot(1, 2, 1) # 1행 2열의 영역에서 첫 번째 영역으로 지정
plt.title('Original Image')
plt.imshow(mpimg.imread('src.png')) # 원본 파일을 읽어서 이미지로 표시

plt.subplot(122) # 1행 2열의 영역에서 두 번째 영역으로 지정 
plt.title('Pseudocolor Image')
dst_img = mpimg.imread('dst.png')
pseudo_img = dst_img [:, :, 0]  # 의사 색상 적용
plt.imshow(pseudo_img) 
plt.show()

