import streamlit as st
import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt

def joint_bilateral_upsampling(low_res_solution, high_res_image, sigma_spatial, sigma_range):
    """
    Joint Bilateral Upsampling implementation
    
    Parameters:
    -----------
    low_res_solution: ndarray
        Low resolution solution to be upsampled
    high_res_image: ndarray
        High resolution guidance image
    sigma_spatial: float
        Spatial parameter for bilateral filter
    sigma_range: float
        Range parameter for bilateral filter
    
    Returns:
    --------
    ndarray: Upsampled solution
    """
    # Compute upsampling factor
    factor = high_res_image.shape[0] // low_res_solution.shape[0]
    
    # Initialize upsampled solution
    upsampled = cv2.resize(low_res_solution, (high_res_image.shape[1], high_res_image.shape[0]), 
                          interpolation=cv2.INTER_LINEAR)
    
    # Create spatial Gaussian kernel
    kernel_size = int(3 * sigma_spatial) | 1  # ensure odd size
    spatial_kernel = np.zeros((kernel_size, kernel_size))
    center = kernel_size // 2
    
    for i in range(kernel_size):
        for j in range(kernel_size):
            diff = (i - center) ** 2 + (j - center) ** 2
            spatial_kernel[i, j] = np.exp(-diff / (2 * sigma_spatial ** 2))
    
    # Normalize kernel
    spatial_kernel /= spatial_kernel.sum()
    
    # Apply joint bilateral filter
    result = np.zeros_like(upsampled)
    pad_size = kernel_size // 2
    
    # Pad images
    padded_guide = np.pad(high_res_image, ((pad_size, pad_size), (pad_size, pad_size)), mode='edge')
    padded_input = np.pad(upsampled, ((pad_size, pad_size), (pad_size, pad_size)), mode='edge')
    
    for i in range(pad_size, padded_guide.shape[0] - pad_size):
        for j in range(pad_size, padded_guide.shape[1] - pad_size):
            # Extract windows
            guide_window = padded_guide[i-pad_size:i+pad_size+1, j-pad_size:j+pad_size+1]
            input_window = padded_input[i-pad_size:i+pad_size+1, j-pad_size:j+pad_size+1]
            
            # Compute range kernel
            range_diff = (guide_window - padded_guide[i, j]) ** 2
            range_kernel = np.exp(-range_diff / (2 * sigma_range ** 2))
            
            # Combine kernels
            combined_kernel = spatial_kernel * range_kernel
            combined_kernel /= combined_kernel.sum() + 1e-10
            
            # Apply filter
            result[i-pad_size, j-pad_size] = (input_window * combined_kernel).sum()
    
    return result

def main():
    st.title("Joint Bilateral Upsampling Viewer")
    
    # Upload images
    high_res = st.file_uploader("Upload high resolution guidance image", type=['png', 'jpg', 'jpeg'])
    low_res = st.file_uploader("Upload low resolution solution", type=['png', 'jpg', 'jpeg'])
    
    if high_res is not None and low_res is not None:
        # Read images
        high_res_img = cv2.imdecode(np.frombuffer(high_res.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        low_res_img = cv2.imdecode(np.frombuffer(low_res.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        
        # Parameters
        sigma_spatial = st.slider("Sigma Spatial", 0.1, 10.0, 5.0, 0.1)
        sigma_range = st.slider("Sigma Range", 0.1, 1.0, 0.1, 0.01)
        
        # Apply JBU
        result = joint_bilateral_upsampling(low_res_img, high_res_img, sigma_spatial, sigma_range)
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("High Resolution Guide")
            st.image(high_res_img, use_column_width=True)
        
        with col2:
            st.subheader("Low Resolution Input")
            st.image(low_res_img, use_column_width=True)
        
        with col3:
            st.subheader("JBU Result")
            st.image(result, use_column_width=True)
        
        # Add visualization of error metrics
        if st.checkbox("Show Error Metrics"):
            # Compute MSE between upsampled result and high-res guide
            mse = np.mean((result - high_res_img) ** 2)
            st.write(f"Mean Squared Error: {mse:.4f}")
            
            # Plot histogram of differences
            fig, ax = plt.subplots()
            ax.hist(result.flatten() - high_res_img.flatten(), bins=50)
            ax.set_title("Histogram of Differences")
            st.pyplot(fig)

if __name__ == "__main__":
    main()