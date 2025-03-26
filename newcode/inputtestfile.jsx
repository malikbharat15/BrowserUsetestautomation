import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const HighRiskComponent = ({ userId }) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('profile');
  const [showModal, setShowModal] = useState(false);
  const modalRef = useRef(null);

  // Dynamic data loading
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(`/api/user/${userId}`);
        setData(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [userId]);

  // Modal focus management
  useEffect(() => {
    if (showModal && modalRef.current) {
      modalRef.current.focus();
    }
  }, [showModal]);

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      setShowModal(false);
    }
  };

  // Complex render with multiple states
  return (
    <div className="user-dashboard">
      {/* 1. Dynamic tabs without proper ARIA */}
      <div className="tabs">
        <div
          className={`tab ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </div>
        <div
          className={`tab ${activeTab === 'settings' ? 'active' : ''}`}
          onClick={() => setActiveTab('settings')}
        >
          Settings
        </div>
      </div>

      {/* 2. Loading/error states without announcements */}
      {isLoading && (
        <div className="loading">
          <div className="spinner"></div>
          Loading...
        </div>
      )}

      {error && (
        <div className="error" style={{ color: '#ff6b6b' }}>
          {error}
        </div>
      )}

      {/* 3. Data table with poor keyboard nav */}
      {data && activeTab === 'profile' && (
        <table className="user-data">
          <tbody>
            {Object.entries(data).map(([key, value]) => (
              <tr key={key}>
                <td>{key}</td>
                <td>
                  {typeof value === 'object'
                    ? JSON.stringify(value)
                    : value}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* 4. Modal with incomplete focus trap */}
      <button
        onClick={() => setShowModal(true)}
        style={{ backgroundColor: '#4CAF50', color: 'white' }}
      >
        Edit Profile
      </button>

      {showModal && (
        <div
          className="modal"
          ref={modalRef}
          tabIndex="-1"
          onKeyDown={handleKeyDown}
          role="dialog"
        >
          <h2>Edit Profile</h2>
          <form>
            <label>
              Name:
              <input type="text" defaultValue={data?.name} />
            </label>

            {/* 5. Form with missing error handling */}
            <label>
              Email:
              <input
                type="email"
                defaultValue={data?.email}
                aria-invalid={!!error}
              />
            </label>

            <div className="button-group">
              <button type="submit">Save</button>
              <button
                type="button"
                onClick={() => setShowModal(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* 6. Hidden interactive element */}
      <div
        className="secret-feature"
        onClick={() => alert('Easter egg!')}
        style={{ position: 'absolute', left: '-9999px' }}
      />
    </div>
  );
};

export default HighRiskComponent;