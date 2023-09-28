import typing as t
import itertools

_headers = {'id': 'ID', 'name': 'Name', 'description': 'Description', 'price': 'Price'}

def print_table(data: t.Iterable[t.Dict[str, str]], headers: t.Dict[str, str]=_headers) -> None:
    keys: t.List[str] = list(headers.keys())
    split_data: t.List[t.Dict[str, t.List[str]]] = []
    max_widths: t.Dict[str, int] = {key: len(value) for key, value in headers.items()}
    for line in data:
        split_line: t.Dict[str, t.List[str]] = {key: str(value).splitlines() for key, value in line.items()}
        for key in keys:
            new_width = max(map(len, split_line.get(key, [''])))
            if new_width > max_widths[key]:
                max_widths[key] = new_width
        split_data.append(split_line)
    for key in keys:
        print(f'{{0:<{max_widths[key]}}}'.format(headers[key]), end='|')  # можно вместо | поставить пробел
    print()
    print('+'.join('-' * v for v in max_widths.values()) + '|')  # разделитель заголовка и тела таблицы
    for row in split_data:
        for parts in itertools.zip_longest(*(row[key] for key in keys)):
            for key, part in zip(keys, parts):
                print(f'{{0:<{max_widths[key]}}}'.format(part if part is not None else ''), end='|')
            print()
        print('+'.join('-' * v for v in max_widths.values()) + '|')  # разделитель строк, если надо

data = [
    {'id': 4381314, 'price': 2128, 'name': 'Weapon # 0', 'description': 'Some description'}, {'id': 3926926, 'price': 1213, 'name': 'Weapon # 1', 'description': 'Some description'}, {'id': 1688252, 'price': 3474, 'name': 'Weapon # 2', 'description': 'Some description'}, {'id': 4662972, 'price': 3801, 'name': 'Weapon # 3', 'description': 'Some description'}, {'id': 3638140, 'price': 1251, 'name': 'Weapon # 4', 'description': 'Some description'}, {'id': 3294777, 'price': 458, 'name': 'Consumables # 5', 'description': 'Some description'}, {'id': 4106723, 'price': 3008, 'name': 'Weapon # 6', 'description': 'Some description'}, {'id': 2962083, 'price': 436, 'name': 'Consumables # 7', 'description': 'Some description'}, {'id': 2907407, 'price': 292, 'name': 'Consumables # 8', 'description': 'Some description'}, {'id': 2759470, 'price': 54720, 'name': 'Aircraft # 9', 'description': 'Some description'}, {'id': 4368623, 'price': 462, 'name': 'Consumables # 10', 'description': 'Some description'}, {'id': 1453738, 'price': 100792, 'name': 'Aircraft # 11', 'description': 'Some description'}, {'id': 4914087, 'price': 73358, 'name': 'Aircraft # 12', 'description': 'Some description'}, {'id': 4414842, 'price': 3650, 'name': 'Armor # 13', 'description': 'Some description'}, {'id': 2006731, 'price': 3237, 'name': 'Weapon # 14', 'description': 'Some description'}, {'id': 2966245, 'price': 3354, 'name': 'Armor # 15', 'description': 'Some description'}, {'id': 3553187, 'price': 153, 'name': 'Consumables # 16', 'description': 'Some description'}, {'id': 2552120, 'price': 70705, 'name': 'Aircraft # 17', 'description': 'Some description'}, {'id': 2685843, 'price': 22926, 'name': 'Vehicle # 18', 'description': 'Some description'}, {'id': 3661179, 'price': 246, 'name': 'Consumables # 19', 'description': 'Some description'}, {'id': 2950431, 'price': 11120, 'name': 'Vehicle # 20', 'description': 'Some description'}, {'id': 3106100, 'price': 2638, 'name': 'Armor # 21', 'description': 'Some description'}, {'id': 2969337, 'price': 1172, 'name': 'Armor # 22', 'description': 'Some description'}, {'id': 2462257, 'price': 3621, 'name': 'Weapon # 23', 'description': 'Some description'}, {'id': 1919433, 'price': 14714, 'name': 'Vehicle # 24', 'description': 'Some description'}, {'id': 4810264, 'price': 176197, 'name': 'Aircraft # 25', 'description': 'Some description'}, {'id': 1592936, 'price': 57401, 'name': 'Aircraft # 26', 'description': 'Some description'}, {'id': 1387526, 'price': 23621, 'name': 'Vehicle # 27', 'description': 'Some description'}, {'id': 3674022, 'price': 1281, 'name': 'Weapon # 28', 'description': 'Some description'}, {'id': 3953814, 'price': 2767, 'name': 'Weapon # 29', 'description': 'Some description'}, {'id': 4998445, 'price': 392, 'name': 'Consumables # 30', 'description': 'Some description'}, {'id': 3351701, 'price': 77154, 'name': 'Aircraft # 31', 'description': 'Some description'}, {'id': 3388299, 'price': 231, 'name': 'Consumables # 32', 'description': 'Some description'}, {'id': 3287455, 'price': 441, 'name': 'Consumables # 33', 'description': 'Some description'}, {'id': 3653930, 'price': 185559, 'name': 'Aircraft # 34', 'description': 'Some description'}, {'id': 3069878, 'price': 4788, 'name': 'Armor # 35', 'description': 'Some description'}, {'id': 4133066, 'price': 10975, 'name': 'Vehicle # 36', 'description': 'Some description'}, {'id': 2307368, 'price': 14200, 'name': 'Vehicle # 37', 'description': 'Some description'}, {'id': 3224438, 'price': 3079, 'name': 'Armor # 38', 'description': 'Some description'}, {'id': 4126810, 'price': 16739, 'name': 'Vehicle # 39', 'description': 'Some description'}, {'id': 4829608, 'price': 2309, 'name': 'Weapon # 40', 'description': 'Some description'}, {'id': 2846357, 'price': 190, 'name': 'Consumables # 41', 'description': 'Some description'}, {'id': 4906519, 'price': 1721, 'name': 'Weapon # 42', 'description': 'Some description'}, {'id': 4304557, 'price': 168, 'name': 'Consumables # 43', 'description': 'Some description'}, {'id': 2190882, 'price': 123, 'name': 'Consumables # 44', 'description': 'Some description'}, {'id': 3357062, 'price': 200946, 'name': 'Aircraft # 45', 'description': 'Some description'}, {'id': 2285379, 'price': 119949, 'name': 'Aircraft # 46', 'description': 'Some description'}, {'id': 1289012, 'price': 2691, 'name': 'Armor # 47', 'description': 'Some description'}, {'id': 1244361, 'price': 263, 'name': 'Consumables # 48', 'description': 'Some description'}, {'id': 3790252, 'price': 3377, 'name': 'Armor # 49', 'description': 'Some description'}, {'id': 2993247, 'price': 245760, 'name': 'Aircraft # 50', 'description': 'Some description'}, {'id': 3788638, 'price': 1690, 'name': 'Weapon # 51', 'description': 'Some description'}, {'id': 2215966, 'price': 1502, 'name': 'Weapon # 52', 'description': 'Some description'}, {'id': 2536016, 'price': 1832, 'name': 'Weapon # 53', 'description': 'Some description'}, {'id': 1422477, 'price': 2681, 'name': 'Weapon # 54', 'description': 'Some description'}, {'id': 1674582, 'price': 1909, 'name': 'Weapon # 55', 'description': 'Some description'}, {'id': 1868372, 'price': 454, 'name': 'Consumables # 56', 'description': 'Some description'}, {'id': 3979237, 'price': 3913, 'name': 'Weapon # 57', 'description': 'Some description'}, {'id': 3392785, 'price': 4440, 'name': 'Armor # 58', 'description': 'Some description'}, {'id': 4133544, 'price': 7136, 'name': 'Vehicle # 59', 'description': 'Some description'}, {'id': 3179907, 'price': 240258, 'name': 'Aircraft # 60', 'description': 'Some description'}, {'id': 3862449, 'price': 174906, 'name': 'Aircraft # 61', 'description': 'Some description'}, {'id': 3460198, 'price': 238, 'name': 'Consumables # 62', 'description': 'Some description'}, {'id': 2662940, 'price': 3712, 'name': 'Armor # 63', 'description': 'Some description'}, {'id': 1366284, 'price': 55277, 'name': 'Aircraft # 64', 'description': 'Some description'}, {'id': 3970431, 'price': 240131, 'name': 'Aircraft # 65', 'description': 'Some description'}, {'id': 3052645, 'price': 390, 'name': 'Consumables # 66', 'description': 'Some description'}, {'id': 1321144, 'price': 159, 'name': 'Consumables # 67', 'description': 'Some description'}, {'id': 3719290, 'price': 10399, 'name': 'Vehicle # 68', 'description': 'Some description'}, {'id': 3590385, 'price': 208, 'name': 'Consumables # 69', 'description': 'Some description'}, {'id': 4555220, 'price': 1625, 'name': 'Weapon # 70', 'description': 'Some description'}, {'id': 2304253, 'price': 8056, 'name': 'Vehicle # 71', 'description': 'Some description'}, {'id': 1462208, 'price': 197070, 'name': 'Aircraft # 72', 'description': 'Some description'}, {'id': 4914994, 'price': 198690, 'name': 'Aircraft # 73', 'description': 'Some description'}, {'id': 4525071, 'price': 4609, 'name': 'Armor # 74', 'description': 'Some description'}, {'id': 1097942, 'price': 3888, 'name': 'Weapon # 75', 'description': 'Some description'}, {'id': 1000795, 'price': 52945, 'name': 'Aircraft # 76', 'description': 'Some description'}, {'id': 4999243, 'price': 67884, 'name': 'Aircraft # 77', 'description': 'Some description'}, {'id': 4174890, 'price': 417, 'name': 'Consumables # 78', 'description': 'Some description'}, {'id': 3042404, 'price': 107690, 'name': 'Aircraft # 79', 'description': 'Some description'}, {'id': 1579397, 'price': 93787, 'name': 'Aircraft # 80', 'description': 'Some description'}, {'id': 1407353, 'price': 4825, 'name': 'Weapon # 81', 'description': 'Some description'}, {'id': 4971198, 'price': 465, 'name': 'Consumables # 82', 'description': 'Some description'}, {'id': 4865489, 'price': 150124, 'name': 'Aircraft # 83', 'description': 'Some description'}, {'id': 1484381, 'price': 2433, 'name': 'Armor # 84', 'description': 'Some description'}, {'id': 4149748, 'price': 1186, 'name': 'Weapon # 85', 'description': 'Some description'}, {'id': 3909545, 'price': 1412, 'name': 'Weapon # 86', 'description': 'Some description'}, {'id': 4040631, 'price': 4011, 'name': 'Weapon # 87', 'description': 'Some description'}, {'id': 4920614, 'price': 3396, 'name': 'Weapon # 88', 'description': 'Some description'}, {'id': 4353404, 'price': 21255, 'name': 'Vehicle # 89', 'description': 'Some description'}, {'id': 4312743, 'price': 447, 'name': 'Consumables # 90', 'description': 'Some description'}, {'id': 1048457, 'price': 428, 'name': 'Consumables # 91', 'description': 'Some description'}, {'id': 2519371, 'price': 2692, 'name': 'Weapon # 92', 'description': 'Some description'}, {'id': 2774074, 'price': 10737, 'name': 'Vehicle # 93', 'description': 'Some description'}, {'id': 2703460, 'price': 6239, 'name': 'Vehicle # 94', 'description': 'Some description'}, {'id': 3856676, 'price': 4821, 'name': 'Weapon # 95', 'description': 'Some description'}, {'id': 3213435, 'price': 379, 'name': 'Consumables # 96', 'description': 'Some description'}, {'id': 4824895, 'price': 248, 'name': 'Consumables # 97', 'description': 'Some description'}, {'id': 1744977, 'price': 1851, 'name': 'Armor # 98', 'description': 'Some description'}, {'id': 4723980, 'price': 4469, 'name': 'Armor # 99', 'description': 'Some description'}, {'id': 1996986, 'price': 1884, 'name': 'Armor # 0', 'description': 'Some description'}, {'id': 2995038, 'price': 2170, 'name': 'Weapon # 1', 'description': 'Some description'}, {'id': 1422148, 'price': 2508, 'name': 'Weapon # 2', 'description': 'Some description'}, {'id': 2570986, 'price': 2896, 'name': 'Armor # 3', 'description': 'Some description'}, {'id': 2675207, 'price': 19673, 'name': 'Vehicle # 4', 'description': 'Some description'}, {'id': 3333391, 'price': 20325, 'name': 'Vehicle # 5', 'description': 'Some description'}, {'id': 2158203, 'price': 187121, 'name': 'Aircraft # 6', 'description': 'Some description'}, {'id': 2932589, 'price': 21918, 'name': 'Vehicle # 7', 'description': 'Some description'}, {'id': 1585845, 'price': 174889, 'name': 'Aircraft # 8', 'description': 'Some description'}, {'id': 1482956, 'price': 216, 'name': 'Consumables # 9', 'description': 'Some description'}, {'id': 1104039, 'price': 9694, 'name': 'Vehicle # 10', 'description': 'Some description'}, {'id': 1748151, 'price': 3609, 'name': 'Weapon # 11', 'description': 'Some description'}, {'id': 2299608, 'price': 137887, 'name': 'Aircraft # 12', 'description': 'Some description'}, {'id': 2113804, 'price': 409, 'name': 'Consumables # 13', 'description': 'Some description'}, {'id': 3815068, 'price': 3301, 'name': 'Weapon # 14', 'description': 'Some description'}, {'id': 2945714, 'price': 166, 'name': 'Consumables # 15', 'description': 'Some description'}, {'id': 1878610, 'price': 13791, 'name': 'Vehicle # 16', 'description': 'Some description'}, {'id': 4407892, 'price': 3420, 'name': 'Armor # 17', 'description': 'Some description'}, {'id': 4547515, 'price': 4105, 'name': 'Armor # 18', 'description': 'Some description'}, {'id': 2720435, 'price': 57261, 'name': 'Aircraft # 19', 'description': 'Some description'}, {'id': 3108849, 'price': 1430, 'name': 'Weapon # 20', 'description': 'Some description'}, {'id': 2702209, 'price': 179, 'name': 'Consumables # 21', 'description': 'Some description'}, {'id': 2939951, 'price': 8856, 'name': 'Vehicle # 22', 'description': 'Some description'}, {'id': 4308975, 'price': 84550, 'name': 'Aircraft # 23', 'description': 'Some description'}, {'id': 2397053, 'price': 300, 'name': 'Consumables # 24', 'description': 'Some description'}, {'id': 4322620, 'price': 93038, 'name': 'Aircraft # 25', 'description': 'Some description'}, {'id': 3212480, 'price': 175988, 'name': 'Aircraft # 26', 'description': 'Some description'}, {'id': 4393216, 'price': 2651, 'name': 'Weapon # 27', 'description': 'Some description'}, {'id': 2369616, 'price': 261, 'name': 'Consumables # 28', 'description': 'Some description'}, {'id': 2294860, 'price': 4842, 'name': 'Weapon # 29', 'description': 'Some description'}, {'id': 3676541, 'price': 3663, 'name': 'Weapon # 30', 'description': 'Some description'}, {'id': 4550540, 'price': 2884, 'name': 'Weapon # 31', 'description': 'Some description'}, {'id': 4847827, 'price': 423, 'name': 'Consumables # 32', 'description': 'Some description'}, {'id': 1872167, 'price': 104801, 'name': 'Aircraft # 33', 'description': 'Some description'}, {'id': 1095216, 'price': 14866, 'name': 'Vehicle # 34', 'description': 'Some description'}, {'id': 1655768, 'price': 471, 'name': 'Consumables # 35', 'description': 'Some description'}, {'id': 4553252, 'price': 147, 'name': 'Consumables # 36', 'description': 'Some description'}, {'id': 2137539, 'price': 4120, 'name': 'Weapon # 37', 'description': 'Some description'}, {'id': 2871299, 'price': 478, 'name': 'Consumables # 38', 'description': 'Some description'}, {'id': 3690413, 'price': 132, 'name': 'Consumables # 39', 'description': 'Some description'}, {'id': 3454108, 'price': 351, 'name': 'Consumables # 40', 'description': 'Some description'}, {'id': 3275554, 'price': 5828, 'name': 'Vehicle # 41', 'description': 'Some description'}, {'id': 2233505, 'price': 23738, 'name': 'Vehicle # 42', 'description': 'Some description'}, {'id': 1181709, 'price': 1612, 'name': 'Weapon # 43', 'description': 'Some description'}, {'id': 4445963, 'price': 3618, 'name': 'Weapon # 44', 'description': 'Some description'}, {'id': 4161789, 'price': 205, 'name': 'Consumables # 45', 'description': 'Some description'}, {'id': 1764862, 'price': 1140, 'name': 'Armor # 46', 'description': 'Some description'}, {'id': 2678336, 'price': 3692, 'name': 'Armor # 47', 'description': 'Some description'}, {'id': 4370722, 'price': 3955, 'name': 'Armor # 48', 'description': 'Some description'}, {'id': 4910397, 'price': 14411, 'name': 'Vehicle # 49', 'description': 'Some description'}, {'id': 2216780, 'price': 266, 'name': 'Consumables # 50', 'description': 'Some description'}, {'id': 3924068, 'price': 3524, 'name': 'Armor # 51', 'description': 'Some description'}, {'id': 4671416, 'price': 146332, 'name': 'Aircraft # 52', 'description': 'Some description'}, {'id': 4678395, 'price': 97660, 'name': 'Aircraft # 53', 'description': 'Some description'}, {'id': 3451188, 'price': 211731, 'name': 'Aircraft # 54', 'description': 'Some description'}, {'id': 4426485, 'price': 4783, 'name': 'Armor # 55', 'description': 'Some description'}, {'id': 3427298, 'price': 14178, 'name': 'Vehicle # 56', 'description': 'Some description'}, {'id': 3535830, 'price': 245903, 'name': 'Aircraft # 57', 'description': 'Some description'}, {'id': 4377087, 'price': 470, 'name': 'Consumables # 58', 'description': 'Some description'}, {'id': 4537359, 'price': 1186, 'name': 'Armor # 59', 'description': 'Some description'}, {'id': 3365380, 'price': 1284, 'name': 'Weapon # 60', 'description': 'Some description'}, {'id': 2250299, 'price': 1330, 'name': 'Armor # 61', 'description': 'Some description'}, {'id': 4722440, 'price': 179836, 'name': 'Aircraft # 62', 'description': 'Some description'}, {'id': 2270146, 'price': 148, 'name': 'Consumables # 63', 'description': 'Some description'}, {'id': 2351451, 'price': 2015, 'name': 'Armor # 64', 'description': 'Some description'}, {'id': 1400011, 'price': 14250, 'name': 'Vehicle # 65', 'description': 'Some description'}, {'id': 1853579, 'price': 2234, 'name': 'Weapon # 66', 'description': 'Some description'}, {'id': 2430762, 'price': 438, 'name': 'Consumables # 67', 'description': 'Some description'}, {'id': 4618696, 'price': 188595, 'name': 'Aircraft # 68', 'description': 'Some description'}, {'id': 1697910, 'price': 254, 'name': 'Consumables # 69', 'description': 'Some description'}, {'id': 2624395, 'price': 158810, 'name': 'Aircraft # 70', 'description': 'Some description'}, {'id': 1955026, 'price': 1615, 'name': 'Armor # 71', 'description': 'Some description'}, {'id': 3719691, 'price': 246218, 'name': 'Aircraft # 72', 'description': 'Some description'}, {'id': 3807767, 'price': 2759, 'name': 'Armor # 73', 'description': 'Some description'}, {'id': 2546212, 'price': 2757, 'name': 'Armor # 74', 'description': 'Some description'}, {'id': 2097724, 'price': 3450, 'name': 'Weapon # 75', 'description': 'Some description'}, {'id': 4443946, 'price': 235883, 'name': 'Aircraft # 76', 'description': 'Some description'}, {'id': 4090286, 'price': 340, 'name': 'Consumables # 77', 'description': 'Some description'}, {'id': 3738780, 'price': 303, 'name': 'Consumables # 78', 'description': 'Some description'}, {'id': 4825023, 'price': 20975, 'name': 'Vehicle # 79', 'description': 'Some description'}, {'id': 2956113, 'price': 12382, 'name': 'Vehicle # 80', 'description': 'Some description'}, {'id': 2654596, 'price': 2337, 'name': 'Weapon # 81', 'description': 'Some description'}, {'id': 1499712, 'price': 3902, 'name': 'Weapon # 82', 'description': 'Some description'}, {'id': 1361791, 'price': 8427, 'name': 'Vehicle # 83', 'description': 'Some description'}, {'id': 2790299, 'price': 4531, 'name': 'Weapon # 84', 'description': 'Some description'}, {'id': 1468382, 'price': 5734, 'name': 'Vehicle # 85', 'description': 'Some description'}, {'id': 2287915, 'price': 216437, 'name': 'Aircraft # 86', 'description': 'Some description'}, {'id': 1482411, 'price': 3921, 'name': 'Weapon # 87', 'description': 'Some description'}, {'id': 1275048, 'price': 3606, 'name': 'Armor # 88', 'description': 'Some description'}, {'id': 1571803, 'price': 1610, 'name': 'Armor # 89', 'description': 'Some description'}, {'id': 4709830, 'price': 2465, 'name': 'Armor # 90', 'description': 'Some description'}, {'id': 2758061, 'price': 11466, 'name': 'Vehicle # 91', 'description': 'Some description'}, {'id': 1493378, 'price': 3066, 'name': 'Armor # 92', 'description': 'Some description'}, {'id': 4092604, 'price': 9912, 'name': 'Vehicle # 93', 'description': 'Some description'}, {'id': 1076235, 'price': 19029, 'name': 'Vehicle # 94', 'description': 'Some description'}, {'id': 4801187, 'price': 332, 'name': 'Consumables # 95', 'description': 'Some description'}, {'id': 1388553, 'price': 1133, 'name': 'Weapon # 96', 'description': 'Some description'}, {'id': 2323614, 'price': 212793, 'name': 'Aircraft # 97', 'description': 'Some description'}, {'id': 3422185, 'price': 1575, 'name': 'Armor # 98', 'description': 'Some description'}, {'id': 2528579, 'price': 10605, 'name': 'Vehicle # 99', 'description': 'Some description'}]
