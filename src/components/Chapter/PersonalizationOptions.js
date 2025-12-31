/**
 * PersonalizationOptions Component
 *./PersonalizationOptions
 * A component that displays hardware-aware content options for registered users.
 * Allows users to see content tailored to their hardware setup and experience level.
 */

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import clsx from 'clsx';
import styles from './PersonalizationOptions.module.css';

const PersonalizationOptions = ({
  userHardwareProfile,
  onProfileChange,
  contentMetadata
}) => {
  const { user } = useAuth();
  const [showOptions, setShowOptions] = useState(false);
  // Use authenticated user's profile if available, otherwise use prop or empty object
  const [selectedProfile, setSelectedProfile] = useState(user || userHardwareProfile || {});

  useEffect(() => {
    // Update selectedProfile when the authenticated user changes
    if (user) {
      setSelectedProfile(user);
    } else {
      setSelectedProfile(userHardwareProfile || {});
    }
  }, [user, userHardwareProfile]);

  const toggleOptions = () => {
    setShowOptions(!showOptions);
  };

  const handleProfileChange = (newProfile) => {
    setSelectedProfile(newProfile);
    onProfileChange && onProfileChange(newProfile);
  };

  // Check if content is compatible with user's hardware
  const isCompatible = () => {
    if (!contentMetadata) return true;

    const requiredHardware = contentMetadata.target_hardware || [];
    if (requiredHardware.length === 0) return true;

    // Use the authenticated user's profile if available, otherwise the selected profile
    const profileToCheck = user || selectedProfile;
    if (!profileToCheck) return true;

    // Simple compatibility check - in a real implementation this would be more sophisticated
    return requiredHardware.some(req =>
      profileToCheck.hardware_type === req ||
      profileToCheck.model === req ||
      profileToCheck.components?.includes(req)
    );
  };

  // Get compatibility message
  const getCompatibilityMessage = () => {
    if (!contentMetadata) return null;

    const requiredHardware = contentMetadata.target_hardware || [];
    if (requiredHardware.length === 0) return null;

    // Use the authenticated user's profile if available, otherwise the selected profile
    const profileToCheck = user || selectedProfile;
    if (!profileToCheck) return null;

    if (isCompatible()) {
      return {
        type: 'success',
        message: 'This content is compatible with your hardware setup!'
      };
    } else {
      return {
        type: 'warning',
        message: `This content requires: ${requiredHardware.join(', ')}. Consider reviewing setup guides.`
      };
    }
  };

  const compatibility = getCompatibilityMessage();

  return (
    <div className={styles.personalizationContainer}>
      <div className={styles.header}>
        <h3 className={styles.title}>Personalization Options</h3>
        <button
          className={styles.toggleButton}
          onClick={toggleOptions}
          aria-label={showOptions ? "Hide options" : "Show options"}
        >
          {showOptions ? '▼' : '▶'}
        </button>
      </div>

      {showOptions && (
        <div className={styles.optionsPanel}>
          {user && (
            <div className={styles.currentProfile}>
              <h4>Your Profile: {user.name || user.email?.split('@')[0]}</h4>
              <div className={styles.profileDetails}>
                <p><strong>Type:</strong> {user.hardware_type || 'N/A'}</p>
                <p><strong>Model:</strong> {user.jetson_model || user.model || 'N/A'}</p>
                <p><strong>Components:</strong> {user.components?.join(', ') || 'N/A'}</p>
                <p><strong>Software:</strong> {user.software_stack?.join(', ') || 'N/A'}</p>
                <p><strong>Experience:</strong> {user.experience_level || 'N/A'}</p>
              </div>
            </div>
          )}

          {compatibility && (
            <div className={clsx(
              styles.compatibilityMessage,
              styles[compatibility.type]
            )}>
              {compatibility.message}
            </div>
          )}

          <div className={styles.suggestedContent}>
            <h4>Suggested Content Based on Your Setup:</h4>
            <ul>
              {(user?.hardware_type === 'jetson' || selectedProfile?.hardware_type === 'jetson') && (
                <li>Hardware-specific examples optimized for Jetson platforms</li>
              )}
              {(user?.software_stack?.includes('ros2') || selectedProfile?.software_stack?.includes('ros2')) && (
                <li>ROS 2 specific code examples and tutorials</li>
              )}
              {(user?.software_stack?.includes('nvidia_isaac') || selectedProfile?.software_stack?.includes('nvidia_isaac')) && (
                <li>NVIDIA Isaac specific implementation details</li>
              )}
              <li>Examples matching your experience level</li>
            </ul>
          </div>
        </div>
      )}

      {compatibility && compatibility.type === 'warning' && (
        <div className={clsx(
          styles.inlineCompatibility,
          styles[compatibility.type]
        )}>
          ⚠️ {compatibility.message}
        </div>
      )}
    </div>
  );
};

export default PersonalizationOptions;