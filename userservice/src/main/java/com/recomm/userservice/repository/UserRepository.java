package com.recomm.userservice.repository;

import org.springframework.stereotype.Repository;
import com.recomm.userservice.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

@Repository
public interface UserRepository extends JpaRepository<User, String>{
    boolean existsById(String id);
}
