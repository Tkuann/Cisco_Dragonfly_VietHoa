class Normalizer:

    def __init__(self):
        self.schools = {
            "Fire": "Hỏa",
            "Ice": "Băng",
            "Frost": "Băng",
            "Lightning": "Lôi",
            "Holy": "Thánh",
            "Blood": "Huyết",
            "Arcane": "Ma Thuật",
            "Nature": "Tự Nhiên",
            "Ender": "Ender",
            "Void": "Hư Không",
            "Eldritch": "Dị Thần",
            "Evocation": "Triệu Hồi"
        }

        self.professions = {
            "Wizard": "Pháp Sư",
            "Mage": "Pháp Sư",
            "Battlemage": "Chiến Pháp Sư",
            "Pyromancer": "Hỏa Thuật Sư",
            "Cryomancer": "Băng Thuật Sư",
            "Electromancer": "Lôi Thuật Sư",
            "Necromancer": "Tử Linh Pháp Sư",
            "Priest": "Giáo Sĩ",
            "Cultist": "Giáo Đồ",
            "Shadowwalker": "Kẻ Bước Trong Bóng Tối",
            "Scarecrow": "Bù Nhìn",
            "Archevoker": "Cổ Triệu Sư"
        }

    def normalize(self, text):
        if not isinstance(text, str):
            return None

        original = text

        exact = {
            "Spawn Egg": "Trứng Triệu Hồi",
            "Upgrade Orb": "Ngọc Cầu Nâng Cấp",
            "Magic Resistance": "Kháng Ma Pháp",
            "Spell Power": "Sức Mạnh Phép Thuật",
            "Cooldown Reduction": "Giảm Hồi Chiêu",
            "Cast Time Reduction": "Giảm Thời Gian Niệm",
            "Max Mana": "Mana Tối Đa",
            "Summon Damage": "Sát Thương Triệu Hồi",
            "Casting Movement Speed": "Tốc Độ Di Chuyển Khi Thi Triển",
            "Potion of Mana": "Thuốc Mana",
            "Splash Potion of Mana": "Thuốc Ném Mana",
            "Lingering Potion of Mana": "Thuốc Kéo Dài Mana",
            "Arrow of Mana": "Mũi Tên Mana"
        }

        if text in exact:
            return exact[text]

        for school_en, school_vi in self.schools.items():
            patterns = {
                f"{school_en} Rune": f"Ngọc Văn {school_vi}",
                f"{school_en} Upgrade Orb": f"Ngọc Cầu Nâng Cấp {school_vi}",
                f"{school_en} Spell Power": f"Sức Mạnh Phép Thuật {school_vi}",
                f"{school_en} Magic Resistance": f"Kháng Ma Pháp {school_vi}",
                f"{school_en} Staff": f"Trượng {school_vi}",
                f"{school_en} Ward Ring": f"Nhẫn Hộ {school_vi}"
            }

            if text in patterns:
                return patterns[text]

        for prof_en, prof_vi in self.professions.items():
            patterns = {
                f"{prof_en} Helmet": f"Mũ {prof_vi}",
                f"{prof_en} Hood": f"Mũ Trùm {prof_vi}",
                f"{prof_en} Hat": f"Mũ {prof_vi}",
                f"{prof_en} Chestplate": f"Áo Giáp {prof_vi}",
                f"{prof_en} Robe": f"Áo Choàng {prof_vi}",
                f"{prof_en} Coat": f"Áo Khoác {prof_vi}",
                f"{prof_en} Leggings": f"Quần Giáp {prof_vi}",
                f"{prof_en} Boots": f"Ủng {prof_vi}",
                f"{prof_en} Spawn Egg": f"Trứng Triệu Hồi {prof_vi}"
            }

            if text in patterns:
                return patterns[text]

        if text.startswith("Ring of "):
            return "Nhẫn " + text.replace("Ring of ", "")

        if text.startswith("Amulet of "):
            return "Bùa Hộ Mệnh " + text.replace("Amulet of ", "")

        if text.startswith("Boots of "):
            return "Ủng " + text.replace("Boots of ", "")

        if text.endswith(" Spawn Egg"):
            name = text.replace(" Spawn Egg", "")
            return f"Trứng Triệu Hồi {name}"

        if text.endswith(" Upgrade Orb"):
            name = text.replace(" Upgrade Orb", "")
            return f"Ngọc Cầu Nâng Cấp {name}"

        if text != original:
            return text

        return None