def detect_context(key):
    key = key.lower()

    if key.startswith("item."):
        return "ITEM"

    if key.startswith("block."):
        return "BLOCK"

    if key.startswith("spell."):
        return "SPELL"

    if key.startswith("effect."):
        return "EFFECT"

    if key.startswith("ui.") or key.startswith("gui.") or ".ui." in key or ".gui." in key:
        return "UI"

    if "tooltip" in key or "description" in key or key.endswith(".desc"):
        return "DESCRIPTION"

    if "advancement" in key:
        return "ADVANCEMENT"

    if key.startswith("death.") or "death" in key:
        return "DEATH"

    return "GENERAL"


def context_instruction(context):
    if context == "ITEM":
        return "Đây là tên vật phẩm. Dịch ngắn gọn, phong cách RPG."

    if context == "BLOCK":
        return "Đây là tên khối trong Minecraft. Dịch ngắn gọn, rõ nghĩa."

    if context == "SPELL":
        return "Đây là tên phép thuật. Dịch theo phong cách RPG Fantasy, ưu tiên Hán Việt."

    if context == "EFFECT":
        return "Đây là tên hiệu ứng trạng thái. Dịch ngắn gọn như tên buff/debuff."

    if context == "UI":
        return "Đây là chữ giao diện. Dịch ngắn, rõ, không văn vẻ."

    if context == "DESCRIPTION":
        return "Đây là mô tả. Dịch tự nhiên, dễ hiểu, giữ đúng ý."

    if context == "ADVANCEMENT":
        return "Đây là thành tựu hoặc mô tả thành tựu. Dịch tự nhiên theo phong cách Minecraft RPG."

    if context == "DEATH":
        return "Đây là thông báo tử vong. Dịch tự nhiên, đúng ngữ cảnh Minecraft."

    return "Dịch sang tiếng Việt theo phong cách Minecraft RPG."