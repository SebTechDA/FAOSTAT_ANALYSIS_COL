
# FAOSTAT Data Cleaning Script
# Sebastian Ramirez Bencardino

# Dataset language: Spanish

# Data quality issues addressed:
# 1. Extra whitespace
# 2. Inconsistent text capitalization
# 3. Special characters and accents
# 4. Missing values in Year
# 5. Items with excessive missing values
# 6. Incorrect data types
# 7. Years outside the expected range (1961–2024)
# 8. Invalid values
# 9. Missing values in Value

import pandas as pd
import numpy as np

def distancia(a, b):
    prev = np.arange(len(b) + 1)
    for i, ca in enumerate(a, 1):
        cur = np.zeros(len(b) + 1, dtype=int); cur[0] = i
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (ca != cb))
        prev = cur
    return prev[-1]

def limpiar(df, col, umbral=10, dist_max=4):
    df[col]=df[col].str.strip()
    df[col]=df[col].str.capitalize()
    tabla = df[col].value_counts().reset_index()
    tabla.columns = [col, 'conteo']

    # 1. Group text values after normalization (without accents or case differences),keeping the most frequent version as the canonical value.
    norm = tabla[col].str.lower().str.normalize('NFKD').str.encode('ascii', 'ignore').str.decode('utf-8')
    canon = tabla.assign(norm=norm).sort_values('conteo', ascending=False).groupby('norm')[col].first()
    df[col] = df[col].replace(dict(zip(tabla[col], norm.map(canon))))

    # 2. Recalculate frequencies and correct possible typos using edit distance.
    tabla = df[col].value_counts().reset_index()
    tabla.columns = [col, 'conteo']
    frecuentes = tabla.loc[tabla['conteo'] >= umbral, col].to_numpy()
    raros = tabla.loc[tabla['conteo'] < umbral, col].to_numpy()

    correcciones = {}
    for v in raros:
        d = np.array([distancia (v, f) for f in frecuentes])
        if d.min() <= dist_max:
            correcciones[v] = frecuentes[d.argmin()]
    return df.replace({col: correcciones})

def eliminar_items_por_vacios(df, col_item='Producto', col_value='Valor', umbral_vacios=130):

    # Remove entire items if they contain more than 130 missing values in the "Valor" column.

    filas_antes = len(df)
    items_antes = df[col_item].nunique()
    
    print(f"\n🔍 Analizando {items_antes} items...")
    print(f"   (Umbral: eliminar si hay más de {umbral_vacios} vacíos)\n")
    
    vacios_por_item = {}
    items_eliminar = []
    
    for item in df[col_item].unique():
        datos_item = df[df[col_item] == item]
        
        vacios_value = (
            datos_item[col_value].isna().sum() + 
            (datos_item[col_value].astype(str).str.strip() == '').sum()
        )
         
        total_vacios = vacios_value 
        vacios_por_item[item] = total_vacios
        
        if total_vacios > umbral_vacios:
            items_eliminar.append(item)
            print(f"   ❌ {item}: {total_vacios} vacíos → ELIMINAR")
    
    df_limpio = df[~df[col_item].isin(items_eliminar)].copy()
    return df_limpio

def rellenar_proporcional(df, col):
    porcentajes = df[col].value_counts(normalize=True)  # Calculate category proportions, Fill missing values by randomly sampling categories according to their observed proportions.
    print(porcentajes)

    vacios = df[col].isna()
    df.loc[vacios, col] = np.random.choice(
        porcentajes.index,      # las categorías
        size=vacios.sum(),      # cuántos vacíos hay
        p=porcentajes.values    # su probabilidad (peso %)
    )
    return df

def rellenar_con_datos_cercanos(df, columna_valor='Valor', columna_tiempo='Año',columnas_grupo=['Producto', 'Elemento'], max_distancia=5, verbose=True):

     # Fill missing values only using data from the same group and nearby years. No new values are generated.
    
    total_nulos = df[columna_valor].isna().sum()
    if total_nulos == 0:
        if verbose:
            print(f"  ✅ {columna_valor}: No hay valores nulos")
        return df
    
    if verbose:
        print(f"  📊 {columna_valor}: {total_nulos} nulos → rellenando con datos cercanos")
    
    nulos_rellenados = 0
    
    for (prod, elem), grupo in df.groupby(columnas_grupo):
        indices_nulos = grupo[grupo[columna_valor].isna()].index
        if len(indices_nulos) == 0:
            continue
        
        mascara_grupo = pd.Series(True, index=df.index)
        for col in columnas_grupo:
            mascara_grupo &= (df[col] == grupo[col].iloc[0])
        
        datos_historicos = df[mascara_grupo & df[columna_valor].notna()]
        if len(datos_historicos) == 0:
            continue
        
        años_historicos = datos_historicos[columna_tiempo].values
        valores_historicos = datos_historicos[columna_valor].values
        
        for idx in indices_nulos:
            año_actual = df.loc[idx, columna_tiempo]
            distancias = np.abs(años_historicos - año_actual)
            
            if distancias.min() <= max_distancia:
                idx_cercano = np.argmin(distancias)
                df.loc[idx, columna_valor] = valores_historicos[idx_cercano]
                nulos_rellenados += 1
    
    if verbose:
        print(f"     ✅ {nulos_rellenados} valores rellenados")
    
    return df

def limpiar_relleno_sospechoso(df, columna_valor='Valor', columna_tiempo='Año',columnas_grupo=['Producto', 'Elemento'], factor_maximo=10, verbose=True):

    # Remove filled values that are greater than N times the neighboring value.
    
    if verbose:
        print(f"  🔍 Buscando rellenos sospechosos (> {factor_maximo}x el vecino)")
    
    n_eliminados = 0
    
    for (prod, elem), grupo in df.groupby(columnas_grupo):
        datos = grupo.sort_values(columna_tiempo)
        for i in range(1, len(datos) - 1):
            idx = datos.index[i]
            valor = df.loc[idx, columna_valor]
            if pd.isna(valor):
                continue
            
            v_ant = datos.iloc[i-1][columna_valor]
            v_sig = datos.iloc[i+1][columna_valor]
            
            if (not pd.isna(v_ant) and valor > v_ant * factor_maximo) or \
               (not pd.isna(v_sig) and valor > v_sig * factor_maximo):
                df.loc[idx, columna_valor] = np.nan
                n_eliminados += 1
    
    if verbose:
        print(f"     ✅ {n_eliminados} valores sospechosos eliminados")
    
    return df

def validar_rangos_con_respaldo(df, valor_minimo=0, año_minimo=1961, año_maximo=2024):
    
    # Validate value and year ranges using Year Code as a backup.
    
    filas_antes = len(df)
    
    print("=" * 60)
    print("VALIDACIÓN COMPLETA CON RESPALDO")
    print("=" * 60)
    
    # 1. Remove negative or zero values from the "Valor" column.
    print(f"\n▶ Validando Value (> {valor_minimo})...")
    ceros = (df['Valor'] <= valor_minimo).sum()
    df = df[df['Valor'] > valor_minimo]
    print(f"  Eliminados: {ceros}")
    
    # 2. Check whether Year is within the allowed range. If it is outside the range, replace it with the value from Year Code.  If it remains outside the allowed range, remove the record.
    print(f"\n▶ Validando Year ({año_minimo}-{año_maximo})...")
    mask_invalido = (df['Año'] < año_minimo) | (df['Año'] > año_maximo)
    print(f"  Years inválidos: {mask_invalido.sum()}")
    
    if mask_invalido.sum() > 0:
        # Replace invalid Year values with Year Code
        df.loc[mask_invalido, 'Año'] = df.loc[mask_invalido, 'Código del año']
        
        # Check whether the replacement values are still invalid
        mask_invalido_aun = (df['Año'] < año_minimo) | (df['Año'] > año_maximo)
        print(f"  Reemplazados con Year Code: {mask_invalido.sum() - mask_invalido_aun.sum()}")
        print(f"  Aún inválidos: {mask_invalido_aun.sum()}")
        
        # Remove records that remain outside the allowed range
        if mask_invalido_aun.sum() > 0:
            df = df[~mask_invalido_aun]
    
   # 3. Handle Null and infinite values
    print(f"\n▶ Validando NaN e infinitos...")
    invalidos = df['Valor'].isna().sum() + np.isinf(df['Valor']).sum()
    df = df[df['Valor'].notna()]
    df = df[~np.isinf(df['Valor'])]
    print(f"  Eliminados: {invalidos}")
    
    filas_despues = len(df)
    
    print(f"\n✅ RESULTADO:")
    print(f"  Filas antes: {filas_antes:,}")
    print(f"  Filas después: {filas_despues:,}")
    print(f"  Eliminadas: {filas_antes - filas_despues:,}")
    print(f"  Retención: {filas_despues/filas_antes*100:.1f}%")
    
    return df
#-----------------------------------------------------------------------------------

pd.set_option('display.max_rows', 500)  
pd.set_option('display.max_columns', None)

df=pd.read_csv("FAOSTAT_Sucio.csv")

# Apply the cleaning function to the selected columns.
for col in ["Ámbito", "Área", "Producto", "Elemento", "Unidad"]:
    df = limpiar(df,col)

df= eliminar_items_por_vacios(df, col_item='Producto', col_value='Valor', umbral_vacios=130) 

mask_nan = df['Año'].isna()
df.loc[mask_nan, 'Año'] = df.loc[mask_nan, 'Código del año'] # Fill missing values in the Year column using Year Code.

# Convert Value, Year, and Year Code columns to numeric data types.
# Replace commas with periods in the Value column to enable numeric conversion.
df['Valor'] = df['Valor'].replace(',', '.', regex=True)
df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
df['Año'] = pd.to_numeric(df['Año'], errors='coerce').astype('Int64')
df['Código del año'] = pd.to_numeric(df['Código del año'], errors='coerce').astype('Int64')

# Mark extremely high values as null (greater than 1e12) to avoid skewing the data.
mask_gigante = df['Valor'] > 1e12
if mask_gigante.sum() > 0:
    print(f"  ⚠️  {mask_gigante.sum():,} valores gigantes (>1e12) eliminados")
    df.loc[mask_gigante, 'Valor'] = np.nan

# Replace negative values with missing values.
df.loc[df['Valor'] < 0, 'Valor'] = np.nan

# Sort the DataFrame by Item and Year to organize the data chronologically for each item.
df = df.sort_values(['Producto', 'Año']).reset_index(drop=True) 

# Fill missing values in the Value column using data from nearby years
# within the same Item and Element group. If no nearby data is available,
# the value remains missing.
for col in ['Valor']:
    df = rellenar_con_datos_cercanos(df, col)

# Identify and remove suspicious values in the Value column that are
# substantially higher than nearby values within the same Item and Element group.
for col in ['Valor']:
    df = limpiar_relleno_sospechoso(df, col)

# Fill remaining missing values in the Unit column proportionally
# according to the distribution of existing values.
for col in ['Unidad']:
    df = rellenar_proporcional(df, col) 

# Validate that Year values are within the allowed range.
# Replace invalid Year values using Year Code as a backup.
# Remove records that remain invalid, as well as missing and infinite values.
df = validar_rangos_con_respaldo(df,valor_minimo=1, año_minimo=1961,año_maximo=2024)

df.to_csv("FAOSTAT_data_cleaning.csv", index=False) # Save the cleaned DataFrame to a CSV file.

print("=" * 60)

print("\n✅ Limpieza completa. Archivo guardado como 'FAOSTAT_limpio.csv'.")

print("=" * 60)

# Use this to calculate descriptive statistics for the Year, Year Code, and Value columns
print("ESTADÍSTICAS DESCRIPTIVAS")
print(df[['Año', 'Código del año', 'Valor']].describe()) 

print(df.info())



