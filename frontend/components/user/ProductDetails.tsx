import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { apiClient } from '../../utils/api';
import { useAuth } from '../../utils/auth';

interface Vehicle {
  id: number;
  model: string;
  type: string;
  description: string;
  images: string[];
}

const ProductDetails: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const { isAuthenticated } = useAuth();
  const [vehicle, setVehicle] = useState<Vehicle | null>(null);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    if (id) {
      fetchVehicleDetails();
    }
  }, [id]);

  const fetchVehicleDetails = async () => {
    try {
      const response = await apiClient.get(`/vehicles/${id}`);
      setVehicle(response.data);
    } catch (error) {
      console.error('Failed to fetch vehicle details', error);
    }
  };

  const handleContactSeller = async () => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    try {
      await apiClient.post('/contact-requests', { vehicleId: id });
      alert('Contact request sent successfully!');
    } catch (error) {
      console.error('Failed to send contact request', error);
    }
  };

  const nextImage = () => {
    if (vehicle && vehicle.images) {
      setCurrentImageIndex((prev) => 
        (prev + 1) % vehicle.images.length
      );
    }
  };

  const prevImage = () => {
    if (vehicle && vehicle.images) {
      setCurrentImageIndex((prev) => 
        prev === 0 ? vehicle.images.length - 1 : prev - 1
      );
    }
  };

  if (!vehicle) return <div>Loading...</div>;

  return (
    <div className="product-details">
      <div className="image-gallery">
        <button onClick={prevImage}>{'<'}>
        <img 
          src={vehicle.images[currentImageIndex]} 
          alt={`${vehicle.model} - Image ${currentImageIndex + 1}`} 
        />
        <button onClick={nextImage}>{'>'}</button>
      </div>

      <div className="vehicle-info">
        <h1>{vehicle.model}</h1>
        <p>Type: {vehicle.type}</p>
        <p>Description: {vehicle.description}</p>
        
        <button 
          onClick={handleContactSeller}
          className="contact-seller-btn"
        >
          Contact Seller
        </button>
      </div>
    </div>
  );
};

export default ProductDetails;
