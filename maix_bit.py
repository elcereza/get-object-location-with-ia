import sensor,image,lcd,time
import KPU as kpu
import ujson

lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.set_hmirror(1)
sensor.run(1)
clock = time.clock()
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
task = kpu.load("/sd/20class.kmodel") 
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)

while(True):
    clock.tick()
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    if code:
        for i in code:
            a = img.draw_rectangle(i.rect())
            
            centroid_x = int(i.w() / 2)
            centroid_y = int(i.h() / 2)
            
            location_x = i.x() + centroid_x
            location_y = i.y() + centroid_y

            percent_location_x = int(location_x * 100 / 320)
            percent_location_y = int(location_y * 100 / 240)
            
            a = img.draw_circle(location_x, location_y, 3, color=(255, 255, 255), fill=True)
            
            json_map = {}
            json_map["x"] = percent_location_x
            json_map["y"] = percent_location_y
            json_percent_location = ujson.dumps(json_map)
            
            print(json_percent_location)
            
            a = lcd.display(img)
            for i in code:
                lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
                lcd.draw_string(i.x(), i.y()+12, '%f'%i.value(), lcd.RED, lcd.WHITE)
    else: 	
        a = lcd.display(img)
a = kpu.deinit(task)
