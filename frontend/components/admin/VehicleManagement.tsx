import React, { useState } from 'react';
import { apiClient } from '../../utils/api';

interface Vehicle {
  id?: number;
  model: string;
  type: string;
  description?: string;
  images?: string[];
}

const VehicleManagement: React.FC = () => {
  const [vehicle, setVehicle] = useState<Vehicle>({
    model: '',
    type: '',
    description: '',
    images: []
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setVehicle(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      const formData = new FormData();
      Array.from(files).forEach(file => {
        formData.append('images', file);
      });

      try {
        const response = await apiClient.post('/vehicles/upload-images', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        setVehicle(prev => ({
          ...prev,
          images: response.data.imageUrls
        }));
      } catch (error) {
        console.error('Image upload failed', error);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.post('/vehicles', vehicle);
      alert('Vehicle added successfully');
      // Reset form or redirect
    } catch (error) {
      console.error('Vehicle creation failed', error);
    }
  };

  return (
    <div>
      <h2>Vehicle Management</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="model"
          value={vehicle.model}
          onChange={handleInputChange}
          placeholder="Vehicle Model"
          required
        />
        <select
          name="type"
          value={vehicle.type}
          onChange={handleInputChange}
          required
        >
          <option value="">Select Vehicle Type</option>
          <option value="car">Car</option>
          <option value="truck">Truck</option>
          <option value="motorcycle">Motorcycle</option>
        </select>
        <textarea
          name="description"
          value={vehicle.description}
          onChange={handleInputChange}
          placeholder="Vehicle Description"
        />
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleImageUpload}
        />
        <button type="submit">Add Vehicle</button>
      </form>
    </div>
  );
};

export default VehicleManagement;
