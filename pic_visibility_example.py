def classify_day_night(images_dir, annotations_path, brightness_threshold=50, hsv_brightness_threshold=0.5):
    # Load annotations
    try:
        with open(annotations_path, 'r') as f:
            coco_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Annotations file not found at {annotations_path}")
        
    # Process images
    for img in coco_data['images']:
        img_path = os.path.join(images_dir, img['file_name'])
        if not os.path.exists(img_path):
            # print(f"Warning: Missing image {img['file_name']}")
            continue
        try:
            with Image.open(img_path) as im:
                # Grayscale metrics
                gray = im.convert('L')
                stat = ImageStat.Stat(gray)
                avg_brightness = stat.mean[0]
                # HSV Value channel
                hsv_image = im.convert('HSV')
                v_values = [v/255.0 for h,s,v in hsv_image.getdata()]
                avg_hsv_brightness = sum(v_values) / len(v_values)
                # Print
                print(img_path)
                print(avg_brightness)
                print(avg_hsv_brightness)
                # Classification
                if (avg_brightness > (2 * brightness_threshold) and
                    avg_hsv_brightness > hsv_brightness_threshold):
                    img['pic_visibility'] = 'day'
                elif (avg_brightness < (2 * brightness_threshold) and
                    avg_hsv_brightness > hsv_brightness_threshold):
                    img['pic_visibility'] = 'shadow'
                else:
                    img['pic_visibility'] = 'night'
                print(img['pic_visibility'])
        except Exception as e:
            print(f"Error processing {img['file_name']}: {str(e)}")
            continue
    # Save updated annotations
    with open(annotations_path, 'w') as f:
        json.dump(coco_data, f, indent=4)
    print(f"Successfully processed {len(coco_data['images'])} images")
