const API_URL = 'http://localhost:8000';

        function showMessage(text, type) {
            const msg = document.getElementById('message');
            msg.innerHTML = `<div class="message message-${type}">${text}</div>`;
            setTimeout(() => msg.innerHTML = '', 5000);
        }

        async function loadPosts() {
            try {
                const res = await fetch(`${API_URL}/posts`);
                const data = await res.json();
                displayPosts(data.data);
            } catch (err) {
                showMessage('Error loading posts: ' + err.message, 'error');
            }
        }

        function displayPosts(posts) {
            const container = document.getElementById('postsContainer');
            if (!posts || posts.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #999;">No posts found</p>';
                return;
            }

            container.innerHTML = posts.map(post => `
                <div class="post-card">
                    <span class="post-status ${post.published ? 'status-published' : 'status-draft'}">
                        ${post.published ? 'Published' : 'Draft'}
                    </span>
                    <h3>${post.title}</h3>
                    <p>${post.content}</p>
                    <div class="post-actions">
                        <button class="btn btn-warning" onclick="editPost(${post.id}, '${post.title.replace(/'/g, "\\'")}', '${post.content.replace(/'/g, "\\'")}', ${post.published})">Edit</button>
                        <button class="btn btn-danger" onclick="deletePost(${post.id})">Delete</button>
                    </div>
                </div>
            `).join('');
        }

        document.getElementById('createForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                title: document.getElementById('title').value,
                content: document.getElementById('content').value,
                published: document.getElementById('published').checked
            };

            try {
                const res = await fetch(`${API_URL}/add_post`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                showMessage('Post created successfully!', 'success');
                e.target.reset();
                loadPosts();
            } catch (err) {
                showMessage('Error creating post: ' + err.message, 'error');
            }
        });

        function editPost(id, title, content, published) {
            document.getElementById('editForm').style.display = 'block';
            document.getElementById('editId').value = id;
            document.getElementById('editTitle').value = title;
            document.getElementById('editContent').value = content;
            document.getElementById('editPublished').checked = published;
            document.getElementById('editForm').scrollIntoView({ behavior: 'smooth' });
        }

        function cancelEdit() {
            document.getElementById('editForm').style.display = 'none';
            document.getElementById('updateForm').reset();
        }

        document.getElementById('updateForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const id = document.getElementById('editId').value;
            const payload = {
                title: document.getElementById('editTitle').value,
                content: document.getElementById('editContent').value,
                published: document.getElementById('editPublished').checked
            };

            try {
                const res = await fetch(`${API_URL}/post/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                showMessage('Post updated successfully!', 'success');
                cancelEdit();
                loadPosts();
            } catch (err) {
                showMessage('Error updating post: ' + err.message, 'error');
            }
        });

        async function deletePost(id) {
            if (!confirm('Are you sure you want to delete this post?')) return;

            try {
                await fetch(`${API_URL}/delete_post/${id}`, { method: 'DELETE' });
                showMessage('Post deleted successfully!', 'success');
                loadPosts();
            } catch (err) {
                showMessage('Error deleting post: ' + err.message, 'error');
            }
        }

        loadPosts();