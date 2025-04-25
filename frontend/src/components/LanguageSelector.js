import React from 'react';
import { Select } from '@/components/ui/select';

const LanguageSelector = ({ selectedLanguage, onLanguageChange }) => {
  const languages = [
    { value: 'en', label: 'English' },
    { value: 'ta', label: 'தமிழ் (Tamil)' },
    { value: 'hi', label: 'हिंदी (Hindi)' }
  ];

  return (
    <div className="mb-4">
      <Select
        value={selectedLanguage}
        onValueChange={onLanguageChange}
        className="w-48"
      >
        {languages.map((lang) => (
          <option key={lang.value} value={lang.value}>
            {lang.label}
          </option>
        ))}
      </Select>
    </div>
  );
};

export default LanguageSelector;