import streamlit as st
import pandas as pd

# إعداد الصفحة وتحديد العنوان
st.set_page_config(page_title="منصة تحليل البيانات", layout="wide")

st.title("لوحة تحكم معالجة وعرض الملفات")
st.write("ارفع ملف Excel أو CSV لتوليد مؤشرات ورسوم بيانية تلقائياً.")

# صندوق رفع الملفات
uploaded_file = st.file_uploader("اختر ملفاً لرفعه", type=["csv", "xlsx"])

if uploaded_file is not None:
    # التحقق من نوع الملف وقراءته
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # بطاقات المؤشرات السريعة (KPIs)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("إجمالي السجلات (الصفوف)", len(df))
        with col2:
            st.metric("عدد الأعمدة", len(df.columns))

        # عرض جدول البيانات
        st.subheader("معاينة البيانات المرفوعة")
        st.dataframe(df, use_container_width=True)

        # استخراج الأعمدة الرقمية لإنشاء رسوم بيانية
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

        if numeric_cols:
            st.subheader("رسم بياني تفاعلي")
            selected_col = st.selectbox("اختر العمود الرقمي المراد تحليله:", numeric_cols)
            st.line_chart(df[selected_col])
        else:
            st.info("الملف المرفوع لا يحتوي على أعمدة رقمية لرسمها.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
