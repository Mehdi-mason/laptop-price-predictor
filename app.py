import os
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='حاسبة أسعار اللابتوبات الذكية',
    page_icon='💻',
    layout='centered',
)

st.markdown(
    """
    <style>
    .main { direction: rtl; text-align: right; }
    div[data-testid="stMarkdownContainer"] { direction: rtl; text-align: right; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title('💻 نظام توقع أسعار الحواسيب المحمولة')
st.write('اختر مواصفات الحاسوب المحمول ليقوم نموذج الذكاء الاصطناعي بتقدير سعره فوراً.')

model_path = 'laptop_price_model.pkl'

if not os.path.exists(model_path):
    st.error('⚠️ لم يتم العثور على ملف النموذج `laptop_price_model.pkl`!')
    st.stop()

model = joblib.load(model_path)

col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox(
        'الشركة المصنعة (Brand)',
        [
            'HP', 'Lenovo', 'Asus', 'Dell', 'Acer', 'MSI', 'Apple', 'Samsung',
            'Infinix', 'Xiaomi', 'Gigabyte', 'LG', 'Honor', 'Realme', 'Fujitsu',
            'Zebronics', 'Ultimus', 'Tecno', 'Wings', 'Chuwi', 'Huawei', 'Microsoft', 'Razer',
        ],
    )

    processor_brand = st.selectbox(
        'فئة المعالج (Processor)',
        [
            'Intel Core i5', 'Intel Core i7', 'Intel Core i3', 'Intel Core i9',
            'AMD Ryzen 5', 'AMD Ryzen 7', 'AMD Ryzen 9', 'AMD Budget',
            'Intel Budget', 'Apple M-Series', 'Other',
        ],
    )

    ram_gb = st.selectbox('حجم الرام (RAM بالـ GB)', [4, 8, 12, 16, 32, 64], index=1)

    ram_type = st.selectbox(
        'نوع الرام (RAM Type)',
        ['DDR4', 'DDR5', 'LPDDR5', 'LPDDR4X', 'LPDDR4', 'Unified', 'DDR3'],
    )

    rom_gb = st.selectbox(
        'سعة التخزين (Storage بالـ GB)',
        [64, 128, 256, 512, 1024, 2048],
        index=3,
        format_func=lambda x: f'{x // 1024} TB ({x} GB)' if x >= 1024 else f'{x} GB',
    )

    rom_type = st.selectbox('نوع التخزين (Storage Type)', ['SSD', 'Hard-Disk'])

with col2:
    gpu_type = st.selectbox(
        'نوع كرت الشاشة (GPU Type)',
        [
            'Intel Integrated', 'NVIDIA RTX', 'NVIDIA GTX/MX',
            'AMD Integrated', 'AMD Dedicated', 'Apple Integrated',
        ],
    )

    gpu_vram_gb = st.selectbox(
        'ذاكرة كرت الشاشة الخارجي (VRAM بالـ GB)', [0, 2, 4, 6, 8, 12, 16], index=0
    )

    display_size = st.selectbox(
        'حجم الشاشة (بالبوصة)', [11.6, 13.3, 14.0, 15.6, 16.0, 16.1, 17.3, 18.0], index=3
    )

    resolution = st.selectbox(
        'دقة الشاشة (Resolution)',
        [
            '1920x1080 (Full HD)', '1366x768 (HD)', '1920x1200 (WUXGA)',
            '2560x1440 (2K QHD)', '2560x1600 (WQXGA)', '2880x1800 (2.8K OLED)',
            '3840x2160 (4K UHD)', '3840x2400 (4K+)',
        ],
    )

    os_clean = st.selectbox(
        'نظام التشغيل (OS)',
        ['Windows 11', 'Windows 10', 'Mac OS', 'Other OS (DOS/Chrome/Ubuntu)'],
    )

    warranty = st.selectbox('مدة الضمان (بالسنوات)', [0, 1, 2, 3], index=1)

spec_rating = st.slider(
    'تقييم المواصفات العام (Spec Rating)', min_value=50.0, max_value=95.0, value=70.0, step=1.0
)

res_dims = resolution.split(' ')[0].split('x')
res_width = float(res_dims[0])
res_height = float(res_dims[1])

if st.button('🔮 احسب السعر المتوقع الآن', use_container_width=True):
    input_df = pd.DataFrame(
        [
            {
                'spec_rating': float(spec_rating),
                'Ram_GB': float(ram_gb),
                'ROM_GB': float(rom_gb),
                'GPU_VRAM_GB': float(gpu_vram_gb),
                'display_size': float(display_size),
                'resolution_width': res_width,
                'resolution_height': res_height,
                'warranty': float(warranty),
                'brand': brand,
                'Processor_Brand': processor_brand,
                'Ram_type': ram_type,
                'ROM_type': rom_type,
                'GPU_Type': gpu_type,
                'OS_Clean': os_clean,
            }
        ]
    )

    predicted_price = model.predict(input_df)[0]
    st.success(f'💰 **السعر التقديري في بيانات التدريب:** {predicted_price:,.0f} روبية هندية (INR)')
    st.info(
        f'💵 **ما يعادله تقريباً:** ~ ${predicted_price / 84:,.0f} دولار أمريكي | ~ {(predicted_price / 84) * 135:,.0f} دينار جزائري (سعر الصرف الرسمي)'
    )