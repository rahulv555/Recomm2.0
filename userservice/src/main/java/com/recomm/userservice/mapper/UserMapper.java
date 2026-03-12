package com.recomm.userservice.mapper;


import com.recomm.userservice.model.User;
import com.recomm.userservice.dto.CreateUserRequestDTO;
import com.recomm.userservice.dto.UserResponseDTO;
import com.recomm.userservice.dto.LoginUserResponseDTO;


public class UserMapper {

    //On user creation
    public static User toModel(CreateUserRequestDTO dto, String userID){
        User user = new User();

        user.setUserID(userID);
        user.setName(dto.getName());
        user.setSmoker(dto.getSmoker());
        user.setDrink_Level(dto.getDrink_level());
        user.setBudget(dto.getBudget());
        user.setDress_Preference(dto.getDress_preference());
        user.setAmbience(dto.getAmbience());
        user.setTransport(dto.getTransport());
        user.setMarital_Status(dto.getMarital_status());
        user.setHijos(dto.getHijos());
        user.setPersonality(dto.getPersonality());
        user.setReligion(dto.getReligion());
        user.setInterest(dto.getInterest());
        user.setActivity(dto.getActivity());
        user.setColor(dto.getColor());
        user.setCuisine(dto.getCuisine());
        user.setHeight(dto.getHeight());
        user.setWeight(dto.getWeight());
        user.setBirth_year(dto.getBirth_year());
        user.setAge(dto.getAge());

        return user;
        
  }

  //Get all user details
  public static UserResponseDTO toResponseDTO(User user){
    UserResponseDTO dto = new UserResponseDTO();

    
    dto.setName(user.getName());
    dto.setSmoker(user.getSmoker());
    dto.setDrink_level(user.getDrink_Level());
    dto.setBudget(user.getBudget());
    dto.setDress_preference(user.getDress_Preference());
    dto.setAmbience(user.getAmbience());
    dto.setTransport(user.getTransport());
    dto.setMarital_status(user.getMarital_Status());
    dto.setHijos(user.getHijos());
    dto.setPersonality(user.getPersonality());
    dto.setReligion(user.getReligion());
    dto.setInterest(user.getInterest());
    dto.setActivity(user.getActivity());
    dto.setColor(user.getColor());
    dto.setCuisine(user.getCuisine());
    dto.setHeight(user.getHeight());
    dto.setWeight(user.getWeight());
    dto.setBirth_year(user.getBirth_year());
    dto.setAge(user.getAge());

    return dto;
  }


  //On login, to check if user exists already or not
    public static LoginUserResponseDTO toLoginResponseDto(boolean userExists) {
        LoginUserResponseDTO dto = new LoginUserResponseDTO();

        dto.setUserExists(userExists);
        return dto;
    }


 
}
