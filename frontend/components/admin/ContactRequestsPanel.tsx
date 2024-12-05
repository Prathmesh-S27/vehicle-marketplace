import React, { useState, useEffect } from 'react';
import { apiClient } from '../../utils/api';

interface ContactRequest {
  id: number;
  userId: number;
  vehicleId: number;
  status: string;
  userName: string;
  vehicleModel: string;
}

const ContactRequestsPanel: React.FC = () => {
  const [requests, setRequests] = useState<ContactRequest[]>([]);

  useEffect(() => {
    fetchContactRequests();
  }, []);

  const fetchContactRequests = async () => {
    try {
      const response = await apiClient.get('/contact-requests');
      setRequests(response.data);
    } catch (error) {
      console.error('Failed to fetch contact requests', error);
    }
  };

  const updateRequestStatus = async (id: number, status: string) => {
    try {
      await apiClient.patch(`/contact-requests/${id}`, { status });
      fetchContactRequests();
    } catch (error) {
      console.error('Failed to update request status', error);
    }
  };

  return (
    <div>
      <h2>Contact Requests</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>User</th>
            <th>Vehicle</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {requests.map(request => (
            <tr key={request.id}>
              <td>{request.id}</td>
              <td>{request.userName}</td>
              <td>{request.vehicleModel}</td>
              <td>{request.status}</td>
              <td>
                <button onClick={() => updateRequestStatus(request.id, 'APPROVED')}>
                  Approve
                </button>
                <button onClick={() => updateRequestStatus(request.id, 'REJECTED')}>
                  Reject
                </button>
              d>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ContactRequestsPanel;
