"""
Message history processing node for the async flow pipeline.
"""
import re
from pocketflow import AsyncNode
from google.genai import types


class ProcessMessageHistory(AsyncNode):
    async def prep_async(self, shared):
        print(f"🔧 [ProcessMessageHistory] Preparing to process {len(shared['message_history'])} messages")
        return {
            "message_history": shared["message_history"],
            "bot_user_id": shared.get("bot_user_id"),
            "table_content_map": shared.get("table_content_map", {})
        }
    
    def _replace_table_placeholders(self, content, table_map):
        """Replaces table placeholders in content with actual table data."""
        placeholder_pattern = r'> `\[daia_replaced_table_(\d+)_(\d+)_as_image\]`'
        
        def replacer(match):
            message_id = match.group(1)
            count = match.group(2)
            key = f"{message_id}_{count}"
            
            if key in table_map:
                print(f"✅ [ProcessMessageHistory] Replacing placeholder for key {key}")
                return table_map[key]
            else:
                print(f"⚠️ [ProcessMessageHistory] No table content found for key {key}, placeholder will remain.")
                return match.group(0)  # Return the original placeholder if no content found

        return re.sub(placeholder_pattern, replacer, content)

    async def exec_async(self, prep_res):
        print(f"⚙️ [ProcessMessageHistory] Processing {len(prep_res['message_history'])} messages")
        table_content_map = prep_res.get("table_content_map", {})
        
        # First pass: convert to intermediate format with author info
        raw_messages = []
        unique_users = set()  # Set to collect unique usernames (excluding bot) 
        
        for i, msg in enumerate(prep_res["message_history"]):
            if msg.author.id == prep_res["bot_user_id"]:
                role = "model"
                content = msg.content.strip()
                author_id = None
                author_name = "Bot"
            else:
                role = "user"
                content = msg.content.strip()
                author_id = msg.author.id
                author_name = msg.author.display_name
                unique_users.add(author_name)  # Add username to set
            
            print(f"  📝 [ProcessMessageHistory] Message {i+1}: {role} - {author_name}: {content[:50]}...")
            
            raw_messages.append({
                "role": role,
                "content": content,
                "author_id": author_id,
                "author_name": author_name if role == "user" else "Bot"
            })
        
        # Second pass: combine and normalize messages
        normalized_history = []
        i = 0
        
        while i < len(raw_messages):
            current = raw_messages[i]
            
            if current["role"] == "model":
                # Combine consecutive model messages
                combined_content = [current["content"]]
                j = i + 1
                while j < len(raw_messages) and raw_messages[j]["role"] == "model":
                    combined_content.append(raw_messages[j]["content"])
                    j += 1
                
                normalized_history.append({
                    "role": "model",
                    "content": "\n".join(combined_content)
                })
                i = j
                
            else:  # user message
                # Combine consecutive user messages from same person
                combined_content = [f"{current['author_name']}: {current['content']}"]
                j = i + 1
                
                while j < len(raw_messages) and raw_messages[j]["role"] == "user":
                    if raw_messages[j]["author_id"] == current["author_id"]:
                        # Same person, combine
                        combined_content.append(raw_messages[j]["content"])
                    else:
                        # Different person, need to insert model separator
                        break
                    j += 1
                
                # If we found different users, handle the gap
                if j < len(raw_messages) and raw_messages[j]["role"] == "user" and raw_messages[j]["author_id"] != current["author_id"]:
                    # Add current combined message
                    normalized_history.append({
                        "role": "user",
                        "content": "\n".join(combined_content)
                    })
                    # Add model separator
                    normalized_history.append({
                        "role": "model", 
                        "content": "..."
                    })
                    i = j
                else:
                    # No gap or end of messages
                    normalized_history.append({
                        "role": "user",
                        "content": "\n".join(combined_content)
                    })
                    i = j
        
        # Third pass: Replace table placeholders in the combined content
        if table_content_map:
            print(f"🔄 [ProcessMessageHistory] Starting third pass for table placeholder replacement")
            for msg in normalized_history:
                original_content = msg["content"]
                msg["content"] = self._replace_table_placeholders(original_content, table_content_map)
                if original_content != msg["content"]:
                    print(f"  ✅ [ProcessMessageHistory] Content updated for role {msg['role']}")

        # Convert to Google AI API format
        formatted_history = []
        print(f"🔄 [ProcessMessageHistory] Converting {len(normalized_history)} normalized messages to API format")
        for i, msg in enumerate(normalized_history):
            print(f"  🔗 [ProcessMessageHistory] API Message {i+1}: {msg['role']} - {msg['content'][:50]}...")
            formatted_history.append(
                types.Content(
                    role=msg["role"],
                    parts=[types.Part(text=msg["content"])])
            )
        
        # Ensure first message is from user
        removed_count = 0
        while formatted_history and formatted_history[0].role == "model":
            formatted_history.pop(0)
            removed_count += 1
        
        if removed_count > 0:
            print(f"🗑️ [ProcessMessageHistory] Removed {removed_count} leading model messages")
        
        print(f"✅ [ProcessMessageHistory] Final formatted history has {len(formatted_history)} messages")
        print(f"👥 [ProcessMessageHistory] Found {len(unique_users)} unique users: {unique_users}")
        print(f"formatted_history:  \n{formatted_history}")
        return {"formatted_history": formatted_history, "unique_users": unique_users}
    
    async def post_async(self, shared, prep_res, exec_res):
        shared["formatted_history"] = exec_res["formatted_history"]
        shared["unique_users"] = exec_res["unique_users"]
        print(f"🔄 [ProcessMessageHistory] Post-processing complete, stored {len(exec_res['formatted_history'])} formatted messages")
        print(f"👥 [ProcessMessageHistory] Stored {len(exec_res['unique_users'])} unique users in shared store")
        return "processed"