import React from 'react';
import { Select } from '@/components/ui/select';

const LanguageSelector = ({ selectedLanguage, onLanguageChange }) => {
  const languages = [
    { value: 'en', label: 'English' },
    { value: 'hi', label: 'हिंदी (Hindi)' },
    { value: 'gu', label: 'ગુજરાતી (Gujarati)' },
    { value: 'mr', label: 'मराठी (Marathi)' },
    { value: 'ta', label: 'தமிழ் (Tamil)' },
    { value: 'te', label: 'తెలుగు (Telugu)' },
    { value: 'kn', label: 'ಕನ್ನಡ (Kannada)' },
    { value: 'bn', label: 'বাংলা (Bengali)' },
    { value: 'ml', label: 'മലയാളം (Malayalam)' },
    { value: 'or', label: 'ଓଡ଼ିଆ (Odia)' },
    { value: 'pa', label: 'ਪੰਜਾਬੀ (Punjabi)' },
    { value: 'as', label: 'অসমীয়া (Assamese)' },
    { value: 'ur', label: 'اردو (Urdu)' },
    { value: 'sa', label: 'संस्कृत (Sanskrit)' },
    { value: 'ne', label: 'नेपाली (Nepali)' },
    { value: 'si', label: 'සිංහල (Sinhala)' },
    { value: 'my', label: 'မြန်မာ (Myanmar)' },
    { value: 'sd', label: 'سنڌي (Sindhi)' },
    { value: 'ks', label: 'کٲشُر (Kashmiri)' },
    { value: 'do', label: 'डोगरी (Dogri)' },
    { value: 'mni', label: 'ꯃꯩꯇꯩꯂꯣꯟ (Manipuri)' },
    { value: 'kok', label: 'कोंकणी (Konkani)' }
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