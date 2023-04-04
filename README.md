# backend

## Database 更動細節與待討論事項
1. 所有的 id 皆改為 uuid
2. BindUser: room_uuid 是否刪除
3. User: self_tag_list, find_tag_list 移至 MR_Member_Tag Table
         liked_uset_list, hated_user_list 移至 MR_Liked_Hated_Member Table
         rcm_user_list 移至 MR_Rcmed_Member Table
4. MatchingEvent: matching_algo 用 String 存, Default = “random” -> 討論此欄位是否要存在 DB 中
5. Group: name 未設定 default
6. MachingRoom: 刪除matching_event_uuid