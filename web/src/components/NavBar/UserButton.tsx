import { useAuth } from "@/context/AuthContext";
import { useToast } from "@/context/ToastContext";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { BiSolidUser } from "react-icons/bi";

export const UserButton = () => {
  const router = useRouter();
  const { showToast } = useToast();
  const { isLoggedIn, isLoading, logout } = useAuth();

  const handleLogoutClick = async () => {
    if (!isLoggedIn) {
      // ログインしていないので，ログインページにリダイレクトする
      showToast('まだログインしていません', 'warning');
      router.push('/login');
      return;
    }

    const result = await logout();

    if (result) {
      // ログアウトに成功したので，ログインページにリダイレクトする
      showToast('ログアウトしました', 'success');
      router.push('/login');
    } else {
      showToast('ログアウトに失敗しました', 'error');
    }
  }
  
  return (
    <div className="dropdown">
      <div tabIndex={0} role="button" className="btn btn-ghost p-2">
        {isLoading
          ? <span className="loading loading-spinner" />
          : <BiSolidUser className="w-6 h-6" />
        }
      </div>
      <ul tabIndex={0} className="dropdown-content menu bg-base-300 rounded-box z-1 w-28 p-2 shadow-sm">
        <li className="btn btn-ghost">
          <Link href={"/login"} className="bg-transparent">Login</Link>
        </li>
        <li className="btn btn-ghost" onClick={handleLogoutClick}>Log out</li>
      </ul>
    </div> 
  );
}

