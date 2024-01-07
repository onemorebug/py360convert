import cv2
import numpy as np
import InvariantTM_rgbdiff as TM

def fit_mask(image_path, template_path, mask_path, mask):
    image = cv2.imread(image_path)
    points, centers = TM.InvariantTM_rgbdiff(image_path, template_path, mask_path)

    translation_x = centers[0][0][0]
    translation_y = centers[0][0][1]
    rotation_angle = points[0][1]
    scale_factor = (points[0][2] / 100)

    mask_center = (mask.shape[1] // 2, mask.shape[0] // 2)

    M = cv2.getRotationMatrix2D(mask_center, rotation_angle, scale_factor)
    M[:, 2] += [translation_x, translation_y]

    transformed_mask = cv2.warpAffine(mask, M, (image.shape[1], image.shape[0]))

    inpainting_result = cv2.inpaint(image, transformed_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    cv2.imshow("Inpainted", inpainting_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



    # # template matching
    #
    # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # template_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # template_gray = mask
    #
    # result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF)
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #
    # # Get the coordinates of the matched region
    # top_left = max_loc
    # w, h = template_gray.shape[::1]
    #
    # # Draw a rectangle around the matched region on the original image
    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv2.rectangle(image, top_left, bottom_right, 255, 2)
    #
    # # Display the result
    # cv2.imshow('Object Detection', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # # find mask contours
    # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    # # fit contour to object
    # chosen_contour = None
    # for contour in contours:
    #     chosen_contour = contour
    #     break
    #
    # M = cv2.moments(chosen_contour)
    # cX = int(M["m10"] / M["m00"])
    # cY = int(M["m01"] / M["m00"])
    #
    # # get rotation, translation, scaling
    # rect = cv2.minAreaRect(chosen_contour)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    #
    # # extract rotation, translation, scaling
    # angle = rect[2]
    # center = rect[0]
    # scale = (box[2, 0] - box[0, 0]) / (box[3, 1] - box[1, 1])
    #
    # # get transformation matrix
    # M = cv2.getRotationMatrix2D(center, angle, scale)
    #
    # # apply transformation to mask
    # fitted_mask = cv2.warpAffine(mask, M, (img.shape[1], img.shape[0]))
    #
    # # Apply the transformation to the mask again with correct translation
    # fitted_mask = cv2.warpAffine(fitted_mask, M, (image.shape[1], image.shape[0]), flags=cv2.INTER_NEAREST)
    #
    # # inpaint mask
    # inpainted_img = cv2.inpaint(img, fitted_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    #
    # cv2.imshow("Inpainted", inpainted_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # cv2.imshow("Mask", fitted_mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    # img = cv2.imread('img/trimmedfloor.png')
    mask = cv2.imread('masks/mask_tripod.png', cv2.IMREAD_GRAYSCALE)
    # template = cv2.imread('masks/', cv2.IMREAD_GRAYSCALE)
    image_path = 'img/floor_trimmed_rot.png'
    template_path = 'img/template_bg.jpg'
    mask_path = 'masks/mask_tripod.png'
    fit_mask(image_path, template_path, mask_path, mask)