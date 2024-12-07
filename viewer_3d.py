import streamlit as st
import numpy as np
import open3d as o3d
from PIL import Image
import io
import matplotlib.pyplot as plt

def visualize_3d_point_cloud(points, colors=None):
    """
    Open3Dを使用してポイントクラウドを可視化する
    
    Parameters:
    -----------
    points : numpy.ndarray
        形状が(N, 3)の点群データ
    colors : numpy.ndarray, optional
        形状が(N, 3)の色データ（RGB）
    """
    # ポイントクラウドの作成
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    if colors is not None:
        pcd.colors = o3d.utility.Vector3dVector(colors)
    
    # ビジュアライザの設定
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False)  # オフスクリーンレンダリング
    vis.add_geometry(pcd)
    
    # カメラパラメータの設定
    ctr = vis.get_view_control()
    ctr.set_zoom(0.8)
    ctr.set_front([0, 0, -1])
    ctr.set_lookat([0, 0, 0])
    ctr.set_up([0, -1, 0])
    
    # レンダリング
    vis.poll_events()
    vis.update_renderer()
    
    # 画像として取得
    image = vis.capture_screen_float_buffer(False)
    vis.destroy_window()
    
    return np.asarray(image)

def main():
    st.title("3D Point Cloud Viewer with Open3D")
    
    # サイドバーのコントロール
    st.sidebar.header("Controls")
    
    # ファイルアップローダー
    uploaded_file = st.sidebar.file_uploader(
        "Upload point cloud file", 
        type=['pcd', 'ply']
    )
    
    if uploaded_file is not None:
        # 一時ファイルとして保存
        with open("temp.ply", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # ポイントクラウドの読み込み
        pcd = o3d.io.read_point_cloud("temp.ply")
        points = np.asarray(pcd.points)
        colors = np.asarray(pcd.colors) if pcd.has_colors() else None
        
        # 点群の基本情報を表示
        st.sidebar.write(f"Number of points: {len(points)}")
        
        # 表示オプション
        point_size = st.sidebar.slider("Point Size", 1, 10, 2)
        background_color = st.sidebar.color_picker("Background Color", "#000000")
        
        # 視点コントロール
        st.sidebar.subheader("View Control")
        rotation_x = st.sidebar.slider("Rotation X", -180, 180, 0)
        rotation_y = st.sidebar.slider("Rotation Y", -180, 180, 0)
        rotation_z = st.sidebar.slider("Rotation Z", -180, 180, 0)
        
        # 3D表示
        if points is not None:
            # 回転行列の計算
            R = o3d.geometry.get_rotation_matrix_from_xyz(
                [np.deg2rad(rotation_x), 
                 np.deg2rad(rotation_y), 
                 np.deg2rad(rotation_z)]
            )
            points_rotated = np.asarray(points) @ R.T
            
            # 可視化
            image = visualize_3d_point_cloud(points_rotated, colors)
            st.image(image, caption="3D Point Cloud", use_column_width=True)
            
            # 統計情報の表示
            if st.checkbox("Show Statistics"):
                st.write("Point Cloud Statistics:")
                st.write(f"Bounding Box: {pcd.get_axis_aligned_bounding_box()}")
                st.write(f"Center: {pcd.get_center()}")
                
                # ヒストグラム表示
                fig, ax = plt.subplots(1, 3, figsize=(15, 5))
                ax[0].hist(points[:, 0], bins=50)
                ax[0].set_title("X Distribution")
                ax[1].hist(points[:, 1], bins=50)
                ax[1].set_title("Y Distribution")
                ax[2].hist(points[:, 2], bins=50)
                ax[2].set_title("Z Distribution")
                st.pyplot(fig)

if __name__ == "__main__":
    main()