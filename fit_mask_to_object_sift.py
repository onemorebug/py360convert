import cv2
import numpy as np

def fit_mask_sift(mask, template, img):
    # get sift keypoints
    sift = cv2.SIFT_create(nfeatures=2000)
    kp_img, desc_img = sift.detectAndCompute(img, None)
    kp_template, desc_templaste = sift.detectAndCompute(template, None)

    # match keypoints
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=100)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc_img, desc_templaste, k=2)

    good_matches = []
    for m,n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    matches_img = cv2.drawMatches(img, kp_img, mask, kp_template, good_matches[:1000], None, None, flags=2)
    cv2.imshow("sdkf2", matches_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    src_points = np.float32([kp_img[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_points = np.float32([kp_template[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    homography, mask = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 2.0)

    result_mask = cv2.warpPerspective(mask, homography, (img.shape[1], img.shape[0]))

    result_mask_binary = cv2.threshold(result_mask, 1, 255, cv2.THRESH_BINARY)[1]
    red_mask = np.zeros_like(img)
    red_mask[:, :] = [0, 0, 255]

    result = np.where(result_mask_binary[:, :, None], red_mask, img)



    # result = cv2.inpaint(img, result_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    # result = cv2.bitwise_and(img, img, mask=result_mask)

    cv2.imshow("sdk2", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    img = cv2.imread('img/trimmedfloor.png')
    template = cv2.imread('masks/template.png')
    mask = cv2.imread('masks/mask_tripod.png', cv2.IMREAD_GRAYSCALE)
    fit_mask_sift(mask, template,  img)