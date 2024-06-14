from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

class Kamera_utama:

        
        def __init__(self):

                self.level_kecepatan_mouse_bergerak = 0.05
                self.kemiringan = -90
                self.hitching = 0

                self.posisi_kamera = Vector3([1.0, 5.0, 5.0])
                self.bagian_depan_kamera = Vector3([0.0, 0.0, -1.0])
                self.bagian_atas_kamera = Vector3([0.0, 10.0, 3.0])
                self.bagian_kanan_kamera = Vector3([1.0, 0.0, 3.0])


        
        def vector_kamera_posisi(self):
                bagian_depan = Vector3([0.0, 0.0, 0.0])
                bagian_depan.x = cos(radians(self.kemiringan) * cos(radians(self.hitching)))
                bagian_depan.y = sin(radians(self.hitching))
                bagian_depan.z = sin(radians(self.kemiringan)) * cos(radians(self.hitching))
        
                self.bagian_depan_kamera = vector.normalise(bagian_depan)
                self.bagian_kanan_kamera = vector.normalise(vector3.cross(self.bagian_depan_kamera, Vector3([0.0, 1.0, 0.0])))
                self.bagian_atas_kamera = vector.normalise(vector3.cross(self.bagian_kanan_kamera, self.bagian_depan_kamera))

        
        def konfigurasi_pergerakan_keyboard(self, direction, velocity):
                if direction == "MAJU":
                        self.posisi_kamera += self.bagian_depan_kamera * velocity
                if direction == "MUNDUR":
                        self.posisi_kamera -= self.bagian_depan_kamera * velocity
                if direction == "KIRI":
                        self.posisi_kamera -= self.bagian_kanan_kamera * velocity
                if direction == "KANAN":
                        self.posisi_kamera += self.bagian_kanan_kamera * velocity
                if direction == "KEATAS":
                        self.posisi_kamera[1] += velocity
                if direction == "KEBAWAH":
                        self.posisi_kamera[1] -= velocity

        def proses_pergerakan_mouse(self, xoffset, yoffset, constrain_hitching=True):
                xoffset *= self.level_kecepatan_mouse_bergerak
                yoffset *= self.level_kecepatan_mouse_bergerak

                self.kemiringan += xoffset
                self.hitching += yoffset

                if constrain_hitching:
                        if self.hitching > 45:
                                self.hitching = 45
                        if self.hitching < -45:
                                self.hitching = -45

                self.vector_kamera_posisi()
        
        def update_posisi_baru(self):
                return self.posisi_kamera        
        
        def call_matrix_view_camera(self):
                return matrix44.create_look_at(self.posisi_kamera, self.posisi_kamera + self.bagian_depan_kamera, self.bagian_atas_kamera)
        

