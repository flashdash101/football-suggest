import React, { useState, useEffect } from 'react';
import player from './assets/player.png';
import MainScreen from './MainScreen';
import axios from 'axios';

const FrontScreen = () => {
  const [selectedOption, setSelectedOption] = useState('');
  const [secondOptions, setSecondOptions] = useState([]);
  const [selectedSecondOption, setSelectedSecondOption] = useState('');
  const [canShowRecommendations, setCanShowRecommendations] = useState(false);
  const [showMainScreen, setShowMainScreen] = useState(false);
  const [playingStyle, setPlayingStyle] = useState('No Style');

  const DefenderValues = ['Fullback', 'Wingback', 'Centreback'];
  const MidfielderValues = ['Defensive Midfielder', 'Central Midfielder', 'Attacking Midfielder'];
  const StrikerValues = ['Winger', 'Attacker'];
  const playingStyles = ['Possession', 'Creative', 'Dribbling', 'Goal Threat', 'High-Press', 'Defensive', 'No Style'];

  const handleSelectChange = (e) => {
    
  
    
    const selectedValue = e.target.value;
    setSelectedOption(selectedValue);
    setSelectedSecondOption(''); // Reset the second dropdown

    if (selectedValue === 'Defender') {
      setSecondOptions([...DefenderValues]);
    } else if (selectedValue === 'Midfielder') {
      setSecondOptions([...MidfielderValues]);
    } else if (selectedValue === 'Forward') {
      setSecondOptions([...StrikerValues]);
    } else {
      setSecondOptions([]);
    }
  };

  const handleSecondSelectChange = (e) => {
    setSelectedSecondOption(e.target.value);
  };

  useEffect(() => {
    setCanShowRecommendations(selectedOption !== '' && selectedSecondOption !== '');
  }, [selectedOption, selectedSecondOption]);

  const handleRecommendationsClick = () => {
    console.log("Recommendations button clicked...getting the api values")
    if (canShowRecommendations) {
      setShowMainScreen(true);
      // determineValues();
    }
  };

  if (showMainScreen) {
    return <MainScreen selectedOption={selectedOption}
      selectedSecondOption={selectedSecondOption}
      playingStyle={playingStyle}
      onBack={() => setShowMainScreen(false)} />;
  }



  return (
    <div className="FrontScreen">
      <h1 className="FrontTitle">Player Recommendation System</h1>
      <img src={player} alt="Player" className="Player" />
      <br />
      <select value={selectedOption} onChange={handleSelectChange} className="Category">
        <option value="">Select</option>
        <option value="Defender">Defender</option>
        <option value="Midfielder">Midfielder</option>
        <option value="Forward">Forward</option>
      </select>
      <br />
      <select 
        value={selectedSecondOption} 
        onChange={handleSecondSelectChange} 
        className="Category"
      >
        <option value="">Select</option>
        {secondOptions.map((option, index) => (
          <option key={index} value={option}>
            {option}
          </option>
        ))}
      </select>
      <br />
      <button 
        className="NextButton" 
        onClick={handleRecommendationsClick} 
        disabled={!canShowRecommendations}
      >
        Get Recommendations
      </button>
        <br />
      <select 
        value={playingStyle} 
        onChange={(e) => setPlayingStyle(e.target.value)} 
        className="Category"
      >
        <option value="">Select Playing Style</option>
        {playingStyles.map((style, index) => (
          <option key={index} value={style}>
            {style}
          </option>
        ))}
      </select>
    </div>
  );
};

export default FrontScreen;