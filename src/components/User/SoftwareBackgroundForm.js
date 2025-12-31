import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import clsx from 'clsx';
import styles from './SoftwareBackgroundForm.module.css';

const SoftwareBackgroundForm = ({
  initialData = {},
  onSubmit,
  onCancel,
  submitButtonText = "Save Profile",
  isSubmitting: externalIsSubmitting = false
}) => {
  const { user, updateProfile } = useAuth();
  const [formData, setFormData] = useState({
    software_stack: initialData.software_stack || [],
    experience_level: initialData.experience_level || 'intermediate',
    programming_languages: initialData.programming_languages || [],
    frameworks: initialData.frameworks || [],
    development_tools: initialData.development_tools || [],
    ...initialData
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(externalIsSubmitting);

  const programmingLanguages = [
    { value: 'python', label: 'Python' },
    { value: 'c++', label: 'C++' },
    { value: 'c', label: 'C' },
    { value: 'javascript', label: 'JavaScript' },
    { value: 'typescript', label: 'TypeScript' },
    { value: 'rust', label: 'Rust' },
    { value: 'go', label: 'Go' },
    { value: 'java', label: 'Java' }
  ];

  const frameworks = [
    { value: 'ros2', label: 'ROS 2' },
    { value: 'nvidia_isaac', label: 'NVIDIA Isaac' },
    { value: 'tensorflow', label: 'TensorFlow' },
    { value: 'pytorch', label: 'PyTorch' },
    { value: 'opencv', label: 'OpenCV' },
    { value: 'docker', label: 'Docker' },
    { value: 'kubernetes', label: 'Kubernetes' },
    { value: 'react', label: 'React' },
    { value: 'vue', label: 'Vue.js' },
    { value: 'angular', label: 'Angular' }
  ];

  const developmentTools = [
    { value: 'git', label: 'Git' },
    { value: 'vscode', label: 'VS Code' },
    { value: 'pycharm', label: 'PyCharm' },
    { value: 'clion', label: 'CLion' },
    { value: 'docker', label: 'Docker' },
    { value: 'jupyter', label: 'Jupyter Notebook' },
    { value: 'colab', label: 'Google Colab' },
    { value: 'github', label: 'GitHub' }
  ];

  const experienceLevels = [
    { value: 'beginner', label: 'Beginner' },
    { value: 'intermediate', label: 'Intermediate' },
    { value: 'advanced', label: 'Advanced' }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: ''
      }));
    }
  };

  const handleArrayToggle = (field, value) => {
    setFormData(prev => {
      const currentArray = prev[field] || [];
      const newArray = currentArray.includes(value)
        ? currentArray.filter(item => item !== value)
        : [...currentArray, value];

      return {
        ...prev,
        [field]: newArray
      };
    });
  };

  const validateForm = () => {
    const newErrors = {};
    setErrors(newErrors);
    return true; // Always valid for now
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (validateForm()) {
      setIsSubmitting(true);

      // If user is authenticated, update profile via API
      if (user && updateProfile) {
        const result = await updateProfile(formData);

        if (result.success) {
          onSubmit && onSubmit(formData);
        } else {
          setErrors({ submit: result.error || 'Failed to update profile' });
        }
      } else {
        // If not authenticated, just call onSubmit callback
        onSubmit && onSubmit(formData);
      }

      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.formContainer}>
      <h3 className={styles.formTitle}>Software Background Information</h3>
      <p className={styles.formSubtitle}>
        Help us personalize your learning experience by sharing your software background
      </p>

      <form onSubmit={handleSubmit} className={styles.form}>
        {errors.submit && (
          <div className={styles.errorText}>{errors.submit}</div>
        )}

        <div className={styles.formGroup}>
          <label className={styles.label}>
            Programming Languages
          </label>
          <div className={styles.checkboxGroup}>
            {programmingLanguages.map(lang => (
              <label key={lang.value} className={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={(formData.programming_languages || []).includes(lang.value)}
                  onChange={() => handleArrayToggle('programming_languages', lang.value)}
                  className={styles.checkbox}
                />
                <span className={styles.checkboxText}>{lang.label}</span>
              </label>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.label}>
            Frameworks & Libraries
          </label>
          <div className={styles.checkboxGroup}>
            {frameworks.map(framework => (
              <label key={framework.value} className={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={(formData.frameworks || []).includes(framework.value)}
                  onChange={() => handleArrayToggle('frameworks', framework.value)}
                  className={styles.checkbox}
                />
                <span className={styles.checkboxText}>{framework.label}</span>
              </label>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.label}>
            Development Tools
          </label>
          <div className={styles.checkboxGroup}>
            {developmentTools.map(tool => (
              <label key={tool.value} className={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={(formData.development_tools || []).includes(tool.value)}
                  onChange={() => handleArrayToggle('development_tools', tool.value)}
                  className={styles.checkbox}
                />
                <span className={styles.checkboxText}>{tool.label}</span>
              </label>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.label}>
            Experience Level
          </label>
          <div className={styles.radioGroup}>
            {experienceLevels.map(level => (
              <label key={level.value} className={styles.radioLabel}>
                <input
                  type="radio"
                  name="experience_level"
                  value={level.value}
                  checked={formData.experience_level === level.value}
                  onChange={(e) => handleInputChange('experience_level', e.target.value)}
                  className={styles.radio}
                />
                <span className={styles.radioText}>{level.label}</span>
              </label>
            ))}
          </div>
        </div>

        <div className={styles.buttonGroup}>
          <button
            type="submit"
            disabled={isSubmitting}
            className={clsx(styles.submitButton, isSubmitting && styles.submitButtonDisabled)}
          >
            {isSubmitting ? 'Saving...' : submitButtonText}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className={styles.cancelButton}
              disabled={isSubmitting}
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default SoftwareBackgroundForm;