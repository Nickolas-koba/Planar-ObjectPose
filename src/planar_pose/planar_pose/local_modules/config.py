from sensor_msgs.msg import PointCloud2, Image, CameraInfo
import cv2

# Referência do frame para a estimativa de pose
frame_id = 'camera_color_optical_frame'  # Para a Astra, o nome pode ser 'camera_color_optical_frame'

# Tópico da imagem para detecção de objetos
image_sub = {
    'topic': '/camera/color/image_raw',  # Astra publica imagem colorida no tópico '/camera/color/image_raw'
    'type': Image
}

# Tópico da nuvem de pontos para recuperar
# as localizações 3D
pc_sub = {
    'topic': '/camera/depth/points',  # Astra publica a nuvem de pontos no tópico '/camera/depth/points'
    'type': PointCloud2
}

to_gray = True  # Converter para imagem em tons de cinza

# Se hold_prev_value for True, ele manterá o valor anterior caso não receba um valor por hold_period
hold_prev_vals = True
if hold_prev_vals:
    hold_period = 5  # em segundos

# Tópico das informações da câmera para recuperar a matriz da câmera
cam_info_sub = {
    'topic': '/camera/color/camera_info',  # Astra publica as informações da câmera no tópico '/camera/color/camera_info'
    'type': CameraInfo
}

# Garantir que todos os tópicos tenham a mesma resolução
assert image_sub['topic'].split('/')[1] == pc_sub['topic'].split('/')[1], 'Os tópicos de imagem e nuvem de pontos têm resolução diferente'  # noqa: E501
assert image_sub['topic'].split('/')[1] == cam_info_sub['topic'].split('/')[1], 'Os tópicos de imagem e informações da câmera têm resolução diferente'  # noqa: E501

# Caminho contendo imagens de objetos de consulta
object_path = '/home/nickolas/catkin_ws/src/planar_pose/objects'
# Nome dos objetos correspondentes aos arquivos sem extensão
# Exemplo: book-1.jpg corresponde a book-1
objects = ['book-1', 'chat']

# Quantidade mínima de correspondências necessárias para considerar um objeto detectado
min_match_count = 15

# Definindo o detector-descritor e o
# algoritmo de correspondência
detector_descriptor = cv2.SIFT_create()
matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5),
                                dict(checks=50)).knnMatch
# Se não houver kwargs para o matcher, mantenha como um dict vazio
matcher_kwargs = {'k': 2}

# Visualizar os objetos detectados, se definido como True
show_image = False

# Visualizar a pose dos objetos, se definido como True
viz_pose = True
